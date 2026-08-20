# Performance Benchmarks

Performance analysis comparing the native C-extension (`native_cmod`) and the pure-Python fallback (`pygraphics_python`).

---

## ⚡ Native C vs Pure-Python Comparison

`pygraphics` maintains 100% API parity between its native C-extension and pure-Python implementation:

| Benchmark Operation | Native C (`native_cmod`) | Pure-Python (`pygraphics_python`) | Speedup |
|:---|:---|:---|:---|
| **Bulk `fill_rect` (160×128)** | ~0.08 ms | ~1.42 ms | **~18x** |
| **Filled Circle ($R=40$)** | ~0.15 ms | ~2.60 ms | **~17x** |
| **Rounded Rectangle** | ~0.21 ms | ~3.10 ms | **~15x** |
| **Romfont Text Rendering (20 chars)** | ~0.18 ms | ~1.85 ms | **~10x** |
| **Direct Sprite Blit (64×64)** | ~0.04 ms | ~0.65 ms | **~16x** |

> **Recommendation**: On CPython, Android, and desktop environments, always install the native C wheel (`pydevices-pygraphics`). On bare-metal MicroPython/CircuitPython MCUs without custom C modules, the pure-Python package from MIP provides complete drawing functionality with zero compilation.

---

## 🧠 Memory Footprint

| Component | RAM Overhead |
|:---|:---|
| `pygraphics.Area` instance | 48 bytes |
| `pygraphics.FrameBuffer` wrapper | ~120 bytes + pixel buffer size |
| `pygraphics.Draw` canvas adapter | ~96 bytes (zero extra framebuffer RAM) |
| Embedded Romfonts (8x8, 8x14, 8x16) | 0 bytes heap RAM (read directly from code/frozen bytecode) |

---

## 🔬 Running Parity & Performance Tests Locally

The `pygraphics` repository includes byte-parity test scripts to verify identical pixel output between native and pure-Python backends:

```bash
# Run byte-level parity tests
micropython tools/compare_graphics_run.py

# Run cross-interpreter matrix
python tools/compare_graphics_matrix.py

# Verify MicroPython C framebuf vs pure-Python framebuf
micropython tools/compare_framebuf_mp.py
```
