# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['client3_crip.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\kleberson\\AppData\\Local\\Programs\\Python\\Python314\\Lib\\site-packages\\pyfiglet\\fonts', 'pyfiglet/fonts')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['client.ico'],
)
