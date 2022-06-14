# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['lecto.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pytesseract', '_collections_abc', 'types', '_ctypes', 'enum', 'functools', 'collections', 'heapq', 'keyword', 'operator', 'reprlib', '_weakrefset', 'warnings', 'pwd', 'grp', 'collections.abc', 're', 'sre_compile', 'sre_parse', 'sre_constants', 'copyreg', 'weakref', 'org', '_socket', 'select', 'linecache', 'tokenize', '_bz2', '_lzma', 'pwd', 'grp', 'pyexpat', 'locale', 'pkg_resources.extern.jaraco', 'pkg_resources.extern.more_itertools', '_queue', 'pkg_resources.extern.appdirs', 'win32api', 'win32com.gen_py', 'pkg_resources.extern.packaging', 'traceback', 'pkg_resources.extern.pyparsing', 'org', 'numpy.core._multiarray_umath', 'pickle5', 'numpy.core._multiarray_tests', '_bootlocale', 'numpy.linalg._umath_linalg', 'numpy.fft._pocketfft_internal', 'numpy.random.mtrand', 'numpy.random.bit_generator', 'numpy.random._common', 'backports_abc', '_hashlib', 'numpy.random._bounded_integers', 'numpy.random._mt19937', 'numpy.random._philox', 'numpy.random._pcg64', 'numpy.random._sfc64', 'numpy.random._generator', 'pydantic', 'pydantic.dataclasses', 'backports_abc', 'pydantic.class_validators', 'backports_abc', 'pydantic.errors', 'backports_abc', '_decimal', 'pydantic.typing', 'backports_abc', 'pydantic.utils', 'backports_abc', 'pydantic.version', 'backports_abc', 'pydantic.error_wrappers', 'backports_abc', 'pydantic.json', '_uuid', 'pydantic.color', 'backports_abc', 'pydantic.types', 'backports_abc', 'pydantic.validators', 'backports_abc', 'pydantic.datetime_parse', 'pydantic.fields', 'backports_abc', 'pydantic.main', 'backports_abc', 'pydantic.parse', 'pydantic.schema', 'backports_abc', 'pydantic.networks', 'backports_abc', 'pydantic.annotated_types', 'pydantic.decorator', 'pydantic.env_settings', 'backports_abc', 'pydantic.tools', 'srsly.ujson.ujson', 'encodings.cp437', 'srsly.msgpack._packer', 'srsly.msgpack._unpacker', 'cupy', '_ruamel_yaml', 'cupy', 'cupy', 'torch', 'tensorflow', 'mxnet', 'cupy', 'thinc.backends.numpy_ops', 'cymem.cymem', 'cymem.warnings', 'preshed.maps', 'backports_abc', 'thinc.backends.linalg', 'thinc.backends.blis', 'blis.cy', 'blis.atexit', 'blis.collections', 'blis.enum', 'blis.py', 'blis.numpy', 'murmurhash.mrmr', 'thinc.backends.typing', 'thinc.backends.collections', 'thinc.backends.numpy', 'thinc.backends.blis', 'cupy', 'tensorflow', 'torch', 'cupy', 'torch', 'torch', 'cupy', 'tensorflow', 'h5py', 'mxnet', 'thinc.layers.sparselinear', 'thinc.layers.typing', 'tensorflow', 'spacy.pipeline.pipe', 'spacy.strings', 'backports_abc', 'spacy.srsly', 'spacy.symbols', 'cupy', 'cPickle', 'copy_reg', 'cupy', 'cupy', 'spacy.morphology', 'spacy.numpy', 'spacy.warnings', 'spacy.parts_of_speech', 'spacy.collections', 'spacy.enum', 'spacy.vocab', 'spacy.lexeme', 'spacy.numpy', 'spacy.thinc', 'spacy.warnings', 'spacy.attrs', 'spacy.tokens.doc', 'spacy.tokens.span', 'backports_abc', 'spacy.tokens.numpy', 'spacy.tokens.thinc', 'spacy.tokens.warnings', 'spacy.tokens.copy', 'spacy.tokens.token', 'spacy.tokens.morphanalysis', 'backports_abc', 'backports_abc', 'spacy.tokens.numpy', 'spacy.tokens.thinc', 'spacy.tokens.warnings', 'backports_abc', 'spacy.tokens.copy', 'spacy.tokens.collections', 'spacy.tokens.enum', 'spacy.tokens.itertools', 'spacy.tokens.numpy', 'spacy.tokens.srsly', 'spacy.tokens.thinc', 'spacy.tokens.thinc', 'spacy.tokens.warnings', 'spacy.tokens.span_group', 'spacy.tokens.weakref', 'spacy.tokens.struct', 'spacy.tokens.srsly', 'spacy.tokens.spacy', 'spacy.tokens._retokenize', 'spacy.tokens.thinc', 'spacy.tokens.numpy', 'backports_abc', 'spacy.srsly', 'spacy.thinc', 'spacy.functools', 'spacy.vectors', 'backports_abc', 'spacy.functools', 'spacy.numpy', 'spacy.typing', 'spacy.warnings', 'spacy.enum', 'spacy.srsly', 'spacy.thinc', 'spacy.thinc', 'spacy.thinc', 'preshed.bloom', 'preshed.math', 'preshed.array', 'preshed.copy_reg', 'copy_reg', 'preshed.copyreg', 'spacy.lang.norm_exceptions', 'spacy.tokens._dict_proxies', 'spacy.lang.lex_attrs', 'spacy.pipeline.transition_parser', 'spacy.pipeline._parser_internals.stateclass', 'spacy.pipeline._parser_internals.transition_system', 'spacy.pipeline._parser_internals._beam_utils', 'spacy.pipeline._parser_internals.arc_eager', 'spacy.pipeline._parser_internals.ner', 'spacy.lang.es'],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
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
    name='Lecto',
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
    icon='app.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Lecto',
)
