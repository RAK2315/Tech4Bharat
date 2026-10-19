"""Random-backbone fixtures prove adapter behavior, never inspection accuracy."""
import importlib
import importlib.util
import numpy as np
import pytest


def api():
    name='component_inspector.vision.padim_adapter'
    assert importlib.util.find_spec(name), 'PaDiM adapter not implemented'
    return importlib.import_module(name)


def fixture_adapter():
    module=api()
    import torch
    from anomalib.models.image.padim.torch_model import PadimModel
    torch.set_num_threads(2);torch.manual_seed(4217)
    model=PadimModel(backbone='resnet18',layers=['layer1','layer2','layer3'],pre_trained=False,n_features=100)
    return module.PadimAdapter(model,'fictional',(128,128),
        {'origin':'fictional random weights; software test only','mean':[.485,.456,.406],'std':[.229,.224,.225]})


def test_padim_normalizes_once_and_keeps_backbone_frozen_in_eval():
    adapter=fixture_adapter()
    import torch
    captured=[]
    hook=adapter.model.feature_extractor.register_forward_pre_hook(lambda _m,args: captured.append(args[0].clone()))
    running={k:v.clone() for k,v in adapter.model.feature_extractor.state_dict().items() if 'running_' in k}
    adapter.fit([np.full((128,128,3),.5,np.float32),np.full((128,128,3),.6,np.float32)])
    hook.remove()
    assert captured[0][0,0,0,0].item()==pytest.approx((.5-.485)/.229,abs=1e-6)
    assert all(not p.requires_grad for p in adapter.model.parameters())
    assert not adapter.model.feature_extractor.training
    assert all(torch.equal(v,adapter.model.feature_extractor.state_dict()[k]) for k,v in running.items())


def test_padim_requires_fit_finite_shapes_and_uses_only_valid_roi_max():
    adapter=fixture_adapter()
    query=np.full((128,128,3),.5,np.float32);roi=np.zeros((128,128),bool);roi[32:96,32:96]=True
    with pytest.raises(ValueError,match='fit'):
        adapter.predict_array(query,roi)
    adapter.fit([query,np.full_like(query,.6)])
    score,raw=adapter.predict_array(query,roi)
    assert raw.shape==(128,128) and np.isfinite(raw).all()
    assert score==pytest.approx(float(raw[roi].max()))
    with pytest.raises(ValueError):
        adapter.predict_array(np.full_like(query,np.nan),roi)
    with pytest.raises(ValueError):
        adapter.fit([query])


def test_padim_saved_state_preserves_channels_map_scores_and_rejects_mismatch(tmp_path):
    adapter=fixture_adapter()
    import torch
    rng=np.random.default_rng(22);arrays=[rng.random((128,128,3),dtype=np.float32) for _ in range(3)]
    adapter.fit(arrays)
    query=arrays[0];roi=np.ones((128,128),bool)
    before=adapter.predict_array(query,roi)
    path=tmp_path/'artifact';adapter.save(path,{'fit_manifest_hash':'fictional','fit_ids':['a','b','c']})
    restored=api().PadimAdapter.load(path,expected_recipe='fictional')
    after=restored.predict_array(query,roi)
    assert torch.equal(adapter.model.idx,restored.model.idx)
    assert np.allclose(before[1],after[1],atol=1e-5,rtol=1e-5)
    assert before[0]==pytest.approx(after[0],abs=1e-5,rel=1e-5)
    with pytest.raises(ValueError,match='recipe'):
        api().PadimAdapter.load(path,expected_recipe='wrong')
    with (path/'state.pt').open('ab') as handle:handle.write(b'changed')
    with pytest.raises(ValueError,match='hash'):
        api().PadimAdapter.load(path,expected_recipe='fictional')
