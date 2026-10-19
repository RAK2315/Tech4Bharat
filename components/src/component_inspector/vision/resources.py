"""Supervise one owned local worker with measured memory/time caps."""
import os
from pathlib import Path
import subprocess
import time
import psutil


def run_bounded(command, log_path, *, max_rss_bytes, max_seconds):
    start, peak, status = time.monotonic(), 0, 'completed'
    owned = {}
    max_processes = 0
    def terminate_owned():
        for child in reversed(list(owned.values())):
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
    with Path(log_path).open('x',encoding='utf-8') as log:
        process = subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,
            env={**os.environ,'OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4'})
        try:
            child = psutil.Process(process.pid)
            while process.poll() is None:
                try:
                    members = [child, *child.children(recursive=True)]
                    max_processes = max(max_processes, len(members))
                    sampled = 0
                    for member in members:
                        owned[member.pid] = member
                        try:
                            sampled += member.memory_info().rss
                        except psutil.NoSuchProcess:
                            pass
                    peak = max(peak, sampled)
                except psutil.NoSuchProcess:
                    break
                except psutil.AccessDenied:
                    status = 'monitor_failed'
                    terminate_owned()
                    break
                if peak > max_rss_bytes or time.monotonic()-start > max_seconds:
                    status = 'resource_limit' if peak > max_rss_bytes else 'time_limit'
                    terminate_owned()
                    break
                time.sleep(.05)
            returncode = process.wait()
        finally:
            if process.poll() is None:
                terminate_owned()
                if process.poll() is None:
                    process.kill()
                process.wait()
    if status == 'completed' and returncode != 0:
        status = 'worker_failed'
    return {'status':status,'returncode':returncode,'peak_sampled_rss_bytes':peak,
            'elapsed_seconds':time.monotonic()-start,'rss_cap_bytes':max_rss_bytes,
            'time_cap_seconds':max_seconds,'sample_interval_seconds':.05,
            'measurement_scope':'owned process tree RSS sum','max_observed_processes':max_processes}
