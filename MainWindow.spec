# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['MainWindow.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:/Users/quentin.raball/Documents/Python/CTk/Extractor', './Extractor'),
        ('C:/Users/quentin.raball/Documents/Python/CTk/static', './static'),
        ('C:/Users/quentin.raball/Documents/Python/CTk/themes', './themes'),
        ('C:/Users/quentin.raball/AppData/Local/miniconda3/envs/my-env/Lib/site-packages/customtkinter', 'customtkinter')
    ],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'numpy',
        'matplotlib',
        'os',
        'tkinter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MainWindow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MainWindow',
)