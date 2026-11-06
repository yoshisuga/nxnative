# Bloodstained: Ritual of the Night (`0100BF500207C000`)

Update 1.60 (v851968) over the base game, SDK 7.6.0. ArtPlay / 505 Games, Unreal Engine 4.22 (version 8 paks, version 1 shader code archives) on NVN. Modules `main` (138.6 MB of text), `subsdk0` and `sdk`. Plays on the iPhone at 60 fps (30 on the Switch), with the right colours since the texture keys below.

## What it needs

| Setting | Where | Why |
|---|---|---|
| A second patch area | `dm/tools/patch_nso.py`, the loaders | `main`'s text is longer than one patch area reaches with a B |
| `FPlatformMemory::BaseAllocator` cut (`main+0x5b3a868`) and gate (`main+0x5b3a86c`) | [`patches.py`](patches.py), `dm/host/hle_uemalloc.c` | FMallocBinned3 reserves 37 GB of address space; the host runs Unreal's allocator on a host malloc zone instead |
| Engage's 5 GB block: `mem_reserve 0x140000000`, `mem_alias 0x118000000`, `mem_stack 0x10000000`, `app_pool 0xCD500000` | [`game.tsv`](game.tsv) | 256 MB in front + 4.375 GB alias region + 256 MB stack region + 128 MB heap region; in its first 15 s the game's regions reach alias +2.82 GB |
| `present_interval display` | `game.tsv` | the game asks for present interval 2; Unreal steps by elapsed time, so one frame per display tick plays at normal speed at 60 fps |
| `tex_flush_upload on`, `tex_dirty_upload on` | `game.tsv` | see [Rendering](#rendering) |

## Rendering

- **Resolved: a purple / magenta tint on the characters and props.** Unreal 4.22 streams the top mips of the characters' 256×256 ASTC 6×6 ramp and matcap textures (SPARSE flag 0x20) by writing them from the CPU straight into the texture's storage after the texture was first used, with no NVN copy and no flush. The host kept a GPU-only texture's first, partly written content: all-zero top levels, which ASTC decodes as magenta. Guest memory held the right blocks (`DM_CTL` `passdump`, then `texraw` / `texlist` / `memdump` of the textures bound to Miriam's toon material `978e34f7cd2b4709`, counting zero ASTC blocks). The two texture keys write-protect the registered textures and upload them when the CPU writes. Both are compile-time keys (the host's generated header), so `DM_PROFILE` at run time does not apply them: rebuild the host. Checked on the Mac at the galleon cutscene (59 fps) and on the iPhone, 2026-10-29.

## Versions

- 1.60 (v851968) only. The base game v0 (SDK 5.3, Unreal Engine 4.18, version 4 paks with a pre-version-2 shader archive) also plays on the iPhone, from a provisional profile with different keys: `game_args -SwitchVirtualAddressSpaceSize=4064`, `sys_resource 0x1e00000`, `romfs_marker BloodstainedRotN/Content/Paks/pakchunk0-Switch.pak`, no `patches.py`, and the SDK 5.3 cuts in `dm/tools/sdk_patches.py`. A profile that holds both versions needs these keys per build, which `game.tsv` cannot express yet, so a v0 build keeps its own provisional profile.

## Driving it on the Mac

- About 79 s from launch reaches the galleon cutscene, where Miriam and Johannes show the texture fix; the cutscene needs + to advance.
