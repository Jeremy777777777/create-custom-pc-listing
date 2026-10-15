"""Portable immediate artifact discovery; keep actual names and historical boundaries intact."""
from pathlib import Path


def files_with_suffix(directory,suffix):
    directory=Path(directory)
    if not directory.is_dir(): return []
    paths=sorted(path for path in directory.iterdir()
                 if path.is_file() and path.name.casefold().endswith(suffix.casefold()))
    names=[path.name.casefold() for path in paths]
    if len(set(names))!=len(names):
        raise ValueError('Ambiguous artifact filenames differ only by case: '+str(directory))
    return paths


def current_product_artifacts(root,suffix):
    products=Path(root)/'product generated photo'
    if not products.is_dir(): return []
    return sorted(path for product in products.iterdir() if product.is_dir()
                  for path in files_with_suffix(product,suffix))


def resolve_workbook_path(path):
    """Resolve the actual basename, including callers using Windows-style case aliases."""
    path=Path(path)
    matches=[p for p in files_with_suffix(path.parent,'.xlsx') if p.name.casefold()==path.name.casefold()]
    if len(matches)==1:return matches[0]
    raise FileNotFoundError('Workbook file not found: '+str(path))
