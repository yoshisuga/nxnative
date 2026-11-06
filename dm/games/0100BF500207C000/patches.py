# Bloodstained: Ritual of the Night (0100BF500207C000): the rewriter's patches of this game's own builds (dm/tools/patch_nso.py "Registered patches")
CUTS = {
  # Bloodstained: Ritual of the Night 1.60 (v851968) main (Unreal Engine 4.22): FMallocBinned3 takes 37 GB of address space (its constructor reserves it at main+0x59f4808). FPlatformMemory::
  # BaseAllocator (main+0x5b3a850) mallocs 0x1c28 bytes and constructs them (main+0x5b3a868 → main+0x59f3980). The constructor call is cut, and observation gate OBS_UE_MALLOC (OBS below)
  # puts the host allocator's vtable into the new object, still in x19 (dm/host/hle_uemalloc.c)
  '461b14e505ab955525dc93e0e908c0bc': [
    (0x5b3a868, '46e4fa97', '1f2003d5', 'FPlatformMemory::BaseAllocator: bl 0x59f3980 (FMallocBinned3 constructor, 37 GB of address space) → nop; the host allocator\'s vtable is put in at the gate after it (hle_uemalloc.c)'),
  ],
}
OBS = {
  # Bloodstained: Ritual of the Night 1.60 main: right after the cut constructor call (CUTS above), x19 = the new allocator object; the host writes its vtable there (hle_uemalloc.c)
  '461b14e505ab955525dc93e0e908c0bc': [
    (0x5b3a86c, 21, 'a9417bfd', 'FPlatformMemory::BaseAllocator: the allocator object is in x19, before it is returned: the host puts its vtable in; orig ldp x29, x30, [sp, #0x10]'),
  ],
}
