"""Read-only preservation of scoped research contracts across Git revisions."""
import json
from pathlib import Path
import subprocess


def check_product_research_history(directory):
    directory=Path(directory).resolve()
    if directory.parent.name=='product generated photo':
        return check_research_ledger_history(directory.parent.parent)
    return 0


def check_research_ledger_history(root,base=None,head=None):
    """A scoped ledger cannot disappear/downgrade and revive pre-ledger approval.

    Explicit revision checks use the trusted base. Local checks compare the worktree
    against HEAD when this is a Git checkout. Non-Git scratch fixtures have no
    historical authority; they still receive the ordinary current-input checks.
    """
    if bool(base)!=bool(head): raise ValueError('Research history requires both base and head')
    root=Path(root).resolve()
    def git(*args):
        return subprocess.run(['git',*args],cwd=root,capture_output=True,check=False)
    try:
        top=git('rev-parse','--show-toplevel')
    except FileNotFoundError as error:
        if base or (root/'.git').exists():
            raise ValueError('Git is required to verify research history for this checkout') from error
        return 0
    if top.returncode or Path(top.stdout.decode('utf-8').strip()).resolve()!=root: return 0
    revision=base or 'HEAD'
    tree=git('ls-tree','-rz',revision,'--','product generated photo')
    if tree.returncode:
        if not base and git('rev-parse','--verify','HEAD').returncode: return 0
        raise ValueError('Cannot read trusted research history revision')
    checked=0
    for entry in tree.stdout.split(b'\0'):
        if not entry: continue
        metadata,raw_path=entry.split(b'\t',1);path=raw_path.decode('utf-8')
        parts=Path(path).parts
        if len(parts)!=3 or parts[2]!='research-ledger.json': continue
        blob=git('cat-file','blob',metadata.split()[2].decode())
        if blob.returncode: raise ValueError('Cannot read historical research ledger: '+path)
        previous=json.loads(blob.stdout.decode('utf-8-sig'))
        if not isinstance(previous,dict): continue  # Preserve legacy array compatibility.
        current=root/path
        if not current.is_file():
            raise ValueError('Scoped research ledger removed; historical review cannot become current: '+path)
        data=json.loads(current.read_text(encoding='utf-8-sig'))
        if not isinstance(data,dict):
            raise ValueError('Scoped research ledger downgraded; reconcile evidence without removing its scope: '+path)
        checked+=1
    return checked
