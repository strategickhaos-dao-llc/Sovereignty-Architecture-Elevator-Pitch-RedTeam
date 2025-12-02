# Custom OS Development Guide – 100+ Real Tools & Resources for 2025-2026

**A comprehensive, battle-tested toolkit for building a fully custom, sovereign, from-scratch operating system.**

Everything listed here is public, actively maintained, and has been used by real people to ship real custom OSes—from hobby kernels to commercial products.

---

## 🎯 Quick Start Path

**Fastest route to a bootable custom OS in 90 days:**

1. Read **Phase 0** resources (OSTEP + xv6 lectures)
2. Pick one starter kernel: **BlogOS** (Rust) or **Redox OS** (full Rust stack)
3. Fork it, customize bootloader (Limine), add your features
4. You'll have v0.1 with your name in the source code

**The console is open when you wake up. No rush. Sleep first. Then we ship v0.1.**

---

## Phase 0 – Core Knowledge (Read These First, In Order)

Start here before writing any code. These resources will give you the foundation to understand every decision you make.

1. **[OSDev.org wiki](https://wiki.osdev.org/)** – The bible of OS development. Everything from bootloaders to filesystems.

2. **["Operating Systems: Three Easy Pieces" (OSTEP)](https://pages.cs.wisc.edu/~remzi/OSTEP/)** – Free PDF textbook. Modern, well-written, covers virtualization, concurrency, and persistence.

3. **["The Little Book About OS Development"](https://littleosbook.github.io/)** – Practical guide to building a minimal x86 kernel.

4. **[Bran's Kernel Development Tutorial](http://www.osdever.net/bkerndev/Docs/intro.htm)** – Classic tutorial series for beginners.

5. **["Writing a Simple Operating System from Scratch"](https://www.cs.bham.ac.uk/~exr/lectures/opsys/10_11/lectures/os-dev.pdf)** – Nick Blundell (Cambridge). Excellent PDF covering bootloaders and protected mode.

6. **[MIT 6.S081 / xv6 source + lectures](https://pdos.csail.mit.edu/6.828/2023/schedule.html)** – Teaching OS used at MIT. RISC-V implementation with full lectures available.

7. **[Harvard CS161 – Operating Systems](https://read.seas.harvard.edu/cs161/)** – Operating Systems course (2023-2025) with comprehensive materials.

8. **["Modern Operating Systems" – Tanenbaum 4th ed](https://www.pearson.com/en-us/subject-catalog/p/modern-operating-systems/P200000003295)** – Comprehensive textbook covering OS theory and practice.

9. **[Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)** (Vol 1-3) – Official x86_64 documentation. Essential for low-level work.

10. **[AMD64 Architecture Programmer's Manual](https://www.amd.com/en/support/tech-docs)** – AMD's version of x86_64 documentation.

**Bonus:** **[ARM Architecture Reference Manual](https://developer.arm.com/documentation/)** (if you go ARM)

---

## Phase 1 – Toolchains & Build Systems

You need compilers, linkers, and build tools before writing any OS code.

11. **[GNU Binutils](https://www.gnu.org/software/binutils/)** – `as`, `ld`, `objcopy`, `objdump`, etc. Essential for building any OS.

12. **[GNU GCC cross-compiler](https://wiki.osdev.org/GCC_Cross-Compiler)** – `x86_64-elf-gcc`. Build a cross-compiler to target your OS ABI.

13. **[Clang + LLD (LLVM toolchain)](https://clang.llvm.org/)** – Modern alternative to GCC. Better diagnostics, modular design.

14. **[GNU Make](https://www.gnu.org/software/make/)** – Classic build automation tool.

15. **[CMake](https://cmake.org/)** – Modern build system for larger projects. Better cross-platform support.

16. **[Ninja build](https://ninja-build.org/)** – Fast, lightweight build system. Works well with CMake.

17. **[xorriso](https://www.gnu.org/software/xorriso/)** – ISO creation tool for bootable images.

18. **[grub-mkrescue](https://www.gnu.org/software/grub/)** – Creates GRUB2 bootable ISOs easily.

19. **[QEMU](https://www.qemu.org/)** – Emulation and virtualization. Essential for testing.

20. **[Bochs](http://bochs.sourceforge.net/)** – Debugger-friendly x86 emulator with built-in debugger.

21. **[VirtualBox](https://www.virtualbox.org/)** / **[VMware](https://www.vmware.com/)** – Testing on near-real hardware.

22. **[Docker](https://www.docker.com/)** – Build environment isolation. Reproducible builds.

23. **[Buildroot](https://buildroot.org/)** – Automated rootfs generation for embedded Linux.

24. **[Yocto Project / OpenEmbedded](https://www.yoctoproject.org/)** – Industrial-grade Linux distribution builder.

25. **[Rust + cargo](https://www.rust-lang.org/)** – Memory-safe systems programming. Growing OS ecosystem.

---

## Phase 2 – Bootloaders

How your OS gets loaded into memory and starts executing.

26. **[GRUB2 (multiboot2)](https://www.gnu.org/software/grub/)** – Most popular bootloader. Supports multiboot2 specification.

27. **[Limine](https://github.com/limine-bootloader/limine)** – Modern, simple bootloader with UEFI + BIOS support. Highly recommended.

28. **[systemd-boot](https://www.freedesktop.org/wiki/Software/systemd/systemd-boot/)** – Pure UEFI bootloader. Simple and lightweight.

29. **[rusty-boot](https://github.com/rust-osdev/bootloader)** – Rust bootloader for x86_64. Integrates well with Rust OS projects.

30. **[UEFI firmware (OVMF)](https://github.com/tianocore/tianocore.github.io/wiki/OVMF)** – UEFI firmware for QEMU testing.

---

## Phase 3 – Kernel Blueprints & Starters (Pick One and Fork)

These are complete, working kernels you can study, fork, and customize.

31. **[xv6-riscv](https://github.com/mit-pdos/xv6-riscv)** – MIT teaching kernel. Clean, simple, well-documented.

32. **[SerenityOS kernel](https://github.com/SerenityOS/serenity)** – Modern Unix-like OS with GUI. Active community.

33. **[Redox OS](https://www.redox-os.org/)** – Full Rust OS with microkernel design. Production-quality.

34. **[TempleOS](https://templeos.org/)** – Holy C + unconventional creativity. Unique architecture worth studying.

35. **[Phantom OS](http://phantomos.org/)** – Persistent object-oriented kernel. Novel approach to OS design.

36. **[Theseus](https://github.com/theseus-os/Theseus)** – Rust OS focused on intra-kernel safety and fault isolation.

37. **[BlogOS](https://os.phil-opp.com/)** – Phil Oppermann's "Writing an OS in Rust" tutorial series. Best Rust OS tutorial.

38. **[IntermezzOS](https://intermezzos.github.io/)** – Beginner-friendly Rust kernel tutorial.

39. **[Managarm](https://github.com/managarm/managarm)** – Async kernel in C++ with modern design principles.

40. **[ToaruOS](https://github.com/klange/toaruos)** – Hobby Unix-like with GUI. Impressive one-person project.

---

## Phase 4 – Filesystems

How your OS stores and retrieves data from disks.

41. **[FAT32](https://wiki.osdev.org/FAT)** – Easy to implement, bootable, widely supported.

42. **[ext2](https://wiki.osdev.org/Ext2)** / **[ext4](https://ext4.wiki.kernel.org/)** – Linux filesystems. ext2 is simpler for learning.

43. **[ISO9660](https://wiki.osdev.org/ISO_9660)** – CD-ROM filesystem. Useful for bootable ISOs.

44. **[squashfs](https://www.kernel.org/doc/html/latest/filesystems/squashfs.html)** – Read-only compressed filesystem. Great for embedded systems.

45. **[ZFS](https://openzfs.org/)** – Advanced filesystem with snapshots, compression, and RAID support.

46. **[Btrfs](https://btrfs.wiki.kernel.org/)** – Modern Linux filesystem with CoW and snapshots.

47. **[littlefs](https://github.com/littlefs-project/littlefs)** – Filesystem designed for embedded systems and microcontrollers.

48. **[Rust fatfs crate](https://crates.io/crates/fatfs)** – FAT filesystem implementation in Rust.

49. **libfs implementations in Redox/Serenity** – Study how modern OS projects implement filesystems.

---

## Phase 5 – Drivers & Hardware Abstraction

How your OS talks to hardware devices.

50. **[PCI enumeration code (OSDev wiki)](https://wiki.osdev.org/PCI)** – Detecting and configuring PCI devices.

51. **[AHCI driver template](https://wiki.osdev.org/AHCI)** – SATA disk controller driver.

52. **[NVMe driver template](https://wiki.osdev.org/NVMe)** – Modern SSD interface driver.

53. **[VirtIO drivers](https://docs.oasis-open.org/virtio/virtio/v1.1/virtio-v1.1.html)** – Paravirtualized device drivers for QEMU/KVM.

54. **[USB UHCI/OHCI/EHCI/XHCI stack](https://wiki.osdev.org/USB)** – USB controller drivers for different generations.

55. **[PS/2 keyboard/mouse](https://wiki.osdev.org/PS/2_Keyboard)** – Legacy but simple input device drivers.

56. **[VGA text mode](https://wiki.osdev.org/VGA_Text_Mode)** + **[VBE](https://wiki.osdev.org/VBE)** – Basic graphics output.

57. **[Rust virtio-drivers crate](https://crates.io/crates/virtio-drivers)** – VirtIO drivers in Rust.

58. **[Linux kernel driver sources](https://github.com/torvalds/linux)** – Reference implementation (for study only).

59. **[ACPI parsing libraries (ACPICA)](https://acpica.org/)** – Advanced Configuration and Power Interface support.

---

## Phase 6 – Memory Management

How your OS manages physical and virtual memory.

60. **Physical memory allocator (bitmap or slab)** – Track which pages are free/used.

61. **Virtual memory + paging code (x86_64)** – Set up page tables for virtual addressing.

62. **[Rust alloc crate](https://doc.rust-lang.org/alloc/)** – Standard Rust allocation APIs.

63. **Heap implementation (dlmalloc, jemalloc ports)** – Dynamic memory allocation for kernel/userspace.

64. **[Limine's stivale2 protocol](https://github.com/limine-bootloader/limine/blob/trunk/PROTOCOL.md)** – Modern memory map and boot protocol.

---

## Phase 7 – Scheduling & Syscalls

How your OS runs multiple programs and provides services.

65. **Round-robin preemptive scheduler** – Simple scheduling algorithm to start with.

66. **Syscall interface (int 0x80 vs syscall instruction)** – How userspace programs invoke kernel services.

67. **[Rust no_std + core](https://doc.rust-lang.org/core/)** – Bare-metal Rust without standard library.

68. **[Redox syscall crate](https://crates.io/crates/redox-syscall)** – Redox OS syscall definitions.

69. **[Serenity kernel syscall table](https://github.com/SerenityOS/serenity/tree/master/Kernel/Syscalls)** – Reference implementation of syscalls.

---

## Phase 8 – Userspace & libc

Standard C library and userspace environment.

70. **[newlib](https://sourceware.org/newlib/)** – GNU embedded C library. Popular for hobby OSes.

71. **[musl-libc](https://musl.libc.org/)** – Lightweight, standards-compliant C library.

72. **[uClibc-ng](https://uclibc-ng.org/)** – Small C library for embedded systems.

73. **[Rust core + alloc + std](https://doc.rust-lang.org/std/)** (with `#![no_std]`) – Building Rust userspace.

74. **[Redox relibc](https://gitlab.redox-os.org/redox-os/relibc)** – C library written in Rust for Redox OS.

75. **[Serenity LibC](https://github.com/SerenityOS/serenity/tree/master/Userland/Libraries/LibC)** – SerenityOS C library implementation.

---

## Phase 9 – Full-Stack Distro Blueprints

How to build a complete Linux distribution from scratch (applies to custom OSes too).

76. **[Linux From Scratch (LFS)](http://www.linuxfromscratch.org/)** – Best way to learn packaging and bootstrapping.

77. **[Buildroot configs](https://github.com/buildroot/buildroot/tree/master/configs)** – Thousands of real embedded Linux configurations.

78. **[Yocto layers](https://layers.openembedded.org/)** – meta-openembedded, meta-rust, etc. Modular build system.

79. **[Gentoo Prefix](https://wiki.gentoo.org/wiki/Project:Prefix)** – Bootstrap Gentoo from nothing on any Unix-like system.

80. **[Alpine Linux APK build system](https://wiki.alpinelinux.org/wiki/APKBUILD_Reference)** – Simple, minimal package management.

---

## Phase 10 – Real-World Sovereign/Custom OS Projects (Study Their Repos)

Learn from production-quality custom operating systems.

81. **[Redox OS](https://www.redox-os.org/)** – Full Rust OS with microkernel architecture.

82. **[SerenityOS](https://serenityos.org/)** – Modern Unix-like with beautiful GUI.

83. **[ToaruOS](https://toaruos.org/)** – Complete Unix-like OS with GUI and networking.

84. **[Managarm](https://managarm.org/)** – Async microkernel OS with POSIX compatibility.

85. **[HelenOS](http://www.helenos.org/)** – Microkernel OS with multiserver architecture.

86. **[Genode OS Framework](https://genode.org/)** – Component-based OS framework. Security-focused.

87. **[seL4 microkernel + CAmkES](https://sel4.systems/)** – Formally verified microkernel. Highest security guarantees.

88. **[Fuchsia (Zircon kernel)](https://fuchsia.dev/)** – Google's next-gen OS with async microkernel.

89. **[Haiku OS](https://www.haiku-os.org/)** – BeOS successor. Clean design and responsive UI.

90. **[A2 (Bluebottle/Oberon successor)](https://www.ocp.inf.ethz.ch/wiki/Documentation/ReleaseNotes)** – ETH Zurich research OS.

---

## Bonus: Hard-Mode / Extreme Sovereignty Tools

For absolute sovereignty: control every byte, every build step, every dependency.

91. **Custom linker scripts** – Control exact memory layout and section placement.

92. **Custom ELF loader** – Parse and load executables yourself. Full control over program loading.

93. **Write your own C compiler** – [c4](https://github.com/rswier/c4), [8cc](https://github.com/rui314/8cc), [chibicc](https://github.com/rui314/chibicc) for inspiration.

94. **Write your own assembler** – Study [nasm](https://www.nasm.us/) source. Build your own NASM clone.

95. **Self-hosting toolchain** – [tcc bootstrap](https://bellard.org/tcc/). Compile your compiler with itself.

96. **[Cosmopolitan Libc](https://github.com/jart/cosmopolitan)** – Single binary runs everywhere (Linux, Mac, Windows, BSD).

97. **[MirageOS unikernels](https://mirage.io/)** – Library OS in OCaml. Compile your app directly to a bootable image.

98. **[Unikraft](https://unikraft.org/)** – Modular unikernel framework. Build specialized OSes.

99. **[IncludeOS](https://www.includeos.org/)** – C++ unikernel. Run your app as a VM with no traditional OS.

100. **Your own fork of everything above** – Air-gapped, signed, and built on hardware you control.

---

## 🚀 Getting Started Recommendations

### For Complete Beginners:
1. Start with **OSTEP** (free PDF) and **xv6 lectures**
2. Follow **BlogOS** tutorial step-by-step
3. Use **QEMU** for testing, **Limine** for bootloader
4. Join **OSDev forums** for community support

### For Experienced Developers:
1. Fork **Redox OS** or **SerenityOS**
2. Set up **LLVM/Clang** toolchain
3. Study their build systems and drivers
4. Contribute back or customize for your needs

### For Extreme Sovereignty:
1. Build a **cross-compiler from source**
2. Create custom **linker scripts**
3. Use **Cosmopolitan Libc** for portability
4. Build everything air-gapped on your own hardware

---

## 📚 Additional Resources

- **[OSDev Forums](https://forum.osdev.org/)** – Active community of OS developers
- **[r/osdev subreddit](https://www.reddit.com/r/osdev/)** – OS development discussions
- **[OS Dev Discord](https://discord.gg/RnCtsqD)** – Real-time help and community
- **[Rust OSDev](https://rust-osdev.com/)** – Rust-specific OS development resources

---

## 🎯 90-Day Challenge

**Goal:** Ship a bootable custom OS with your name in the source code.

### Month 1: Foundation
- Read OSTEP (select chapters)
- Complete first 5 BlogOS posts
- Get "Hello World" kernel booting in QEMU

### Month 2: Core Features
- Implement physical memory manager
- Add keyboard driver
- Basic syscall interface

### Month 3: Polish & Extend
- Add filesystem support (FAT32)
- Implement simple scheduler
- Build userspace program

**You can do this.** Thousands of developers have built their own operating systems. The tools are free, the documentation is extensive, and the community is welcoming.

---

**The console is waiting. Fork one of these kernels and start building.**

*No rush. Sleep first. Then we ship v0.1.* 🚀
