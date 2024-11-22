# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:/Aswin Projects/Personal/Selenium/video to text converter/app.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Aswin Projects/Personal/Selenium/video to text converter/backblue.gif', '.'), ('D:/Aswin Projects/Personal/Selenium/video to text converter/fade.gif', '.'), ('D:/Aswin Projects/Personal/Selenium/video to text converter/hts-log.txt', '.'), ('D:/Aswin Projects/Personal/Selenium/video to text converter/index.html', '.'), ('D:/Aswin Projects/Personal/Selenium/video to text converter/hts-cache', 'hts-cache/'), ('D:/Aswin Projects/Personal/Selenium/video to text converter/pagead2.googlesyndication.com', 'pagead2.googlesyndication.com/'), ('D:/Aswin Projects/Personal/Selenium/video to text converter/textify', 'textify/')],
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
    name='app',
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
    icon=['D:\\Aswin Projects\\Personal\\Selenium\\video to text converter\\textify\\img\\icon.ico'],
)
