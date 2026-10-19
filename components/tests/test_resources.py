"""The supervisor must terminate only its owned over-budget child."""
import importlib
import importlib.util
import sys
import pytest


def test_resource_supervisor_rejects_oversized_child_and_records_exit(tmp_path):
    name='component_inspector.vision.resources'
    assert importlib.util.find_spec(name), 'resource supervisor missing'
    api=importlib.import_module(name)
    report=api.run_bounded([sys.executable,'-c','import time; x=bytearray(20_000_000); time.sleep(10)'],
                           tmp_path/'child.log',max_rss_bytes=1,max_seconds=10)
    assert report['status']=='resource_limit'
    assert report['peak_sampled_rss_bytes']>1
    assert report['returncode'] is not None
    good=api.run_bounded([sys.executable,'-c','print("fictional child")'],tmp_path/'good.log',
                        max_rss_bytes=1024**3,max_seconds=10)
    assert good['status']=='completed' and good['returncode']==0
    assert 'fictional child' in (tmp_path/'good.log').read_text()


def test_resource_supervisor_measures_descendants_not_only_python_launcher(tmp_path):
    api=importlib.import_module('component_inspector.vision.resources')
    nested='import time; allocation=bytearray(80_000_000); time.sleep(3)'
    command='import subprocess,sys; subprocess.run([sys.executable,"-c",'+repr(nested)+'])'
    report=api.run_bounded([sys.executable,'-c',command],tmp_path/'nested.log',
                          max_rss_bytes=64*1024**2,max_seconds=15)
    assert report['status']=='resource_limit'
    assert report['peak_sampled_rss_bytes']>64*1024**2
