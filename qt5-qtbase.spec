# Note on packaging .cmake files for plugins:
# Base Qt5${component}Config.cmake file includes all existing Qt5${component}_*Plugin.cmake
# files, which trigger check for presence of plugin module in filesystem.
# Thus, for plugins separated into subpackages, we package plugins .cmake file
# together with module, and the rest of .cmake files in appropriate -devel subpackage.
#
# Conditional build:
%bcond_with	static_libs	# static libraries [incomplete support in .spec]
%bcond_with	bootstrap	# disable features to able to build without installed qt5
# -- build targets
%bcond_without	doc		# Documentation
%bcond_without	qm		# QM translations
# -- features
%bcond_without	cups		# CUPS printing support
%bcond_without	directfb	# DirectFB platform support
%bcond_without	egl		# EGL (EGLFS, minimal EGL) platform support
%bcond_without	gtk		# GTK+ theme integration
%bcond_without	kerberos5	# KRB5 GSSAPI Support
%bcond_without	kms		# KMS platform support
%bcond_without	libinput	# libinput support
%bcond_without	pch		# pch (pre-compiled headers) in qmake
%bcond_without	statx		# build without statx()
%bcond_with	systemd		# logging to journald
%bcond_without	tslib		# tslib support
# -- databases
%bcond_without	freetds		# TDS (Sybase/MS SQL) plugin
%bcond_without	mysql		# MySQL plugin
%bcond_without	odbc		# unixODBC plugin
%bcond_without	pgsql		# PostgreSQL plugin
%bcond_without	sqlite2		# SQLite2 plugin
%bcond_without	sqlite3		# SQLite3 plugin
%bcond_without	ibase		# ibase (InterBase/Firebird) plugin
%bcond_with	db2		# DB2 support
%bcond_with	oci		# OCI (Oracle) support
# -- SIMD CPU instructions
%bcond_with	sse2		# use SSE2 instructions
%bcond_with	sse3		# use SSE3 instructions (since: Intel middle Pentium4, AMD Athlon64)
%bcond_with	ssse3		# use SSSE3 instructions (Intel since Core2, Via Nano)
%bcond_with	sse41		# use SSE4.1 instructions (Intel since middle Core2)
%bcond_with	sse42		# use SSE4.2 instructions (the same)
%bcond_with	avx		# use AVX instructions (Intel since Sandy Bridge, AMD since Bulldozer)
%bcond_with	avx2		# use AVX2 instructions (Intel since Haswell)

%ifnarch %{ix86} %{x8664} x32 sparc sparcv9 alpha ppc
%undefine	with_ibase
%endif
%ifarch	athlon
%define		with_3dnow	1
%endif
%ifarch athlon pentium3 pentium4 %{x8664} x32
%define		with_mmx	1
%endif
%ifarch pentium4 %{x8664} x32
%define		with_sse2	1
%endif
# QTBUG-36129
%ifnarch %{arm} aarch64
%define		with_red_reloc	1
%endif

%if %{with bootstrap}
%undefine	with_doc
%undefine	with_qm
%endif

%define		icu_abi		71
%define		next_icu_abi	%(echo $((%{icu_abi} + 1)))

%define		orgname		qtbase
Summary:	Qt5 - base components
Summary(pl.UTF-8):	Biblioteka Qt5 - podstawowe komponenty
Name:		qt5-%{orgname}
Version:	5.15.7
Release:	1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	5d97a3636ffa080eaf1808a2d8197bae
Source1:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/qttranslations-everywhere-opensource-src-%{version}.tar.xz
# Source1-md5:	6745ce3d167eee999361521d8c9c0277
Patch0:		%{name}-system_cacerts.patch
Patch1:		parallel-install.patch
Patch2:		egl-x11.patch
URL:		https://www.qt.io/
%{?with_directfb:BuildRequires:	DirectFB-devel}
BuildRequires:	EGL-devel
%{?with_ibase:BuildRequires:	Firebird-devel}
%{?with_kms:BuildRequires:	Mesa-libgbm-devel}
BuildRequires:	OpenGL-devel
%{?with_kms:BuildRequires:	OpenGLESv2-devel}
BuildRequires:	Vulkan-Loader-devel
BuildRequires:	at-spi2-core-devel
%{?with_cups:BuildRequires:	cups-devel >= 1.4}
BuildRequires:	dbus-devel >= 1.2
BuildRequires:	double-conversion-devel
BuildRequires:	fontconfig-devel
%{?with_freetds:BuildRequires:	freetds-devel}
BuildRequires:	freetype-devel >= 2.2.0
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	gdb
BuildRequires:	glib2-devel >= 2.0.0
%{?with_gtk:BuildRequires:	gtk+3-devel >= 3.6}
BuildRequires:	harfbuzz-devel >= 1.6.0
%{?with_kerberos5:BuildRequires:	heimdal-devel}
%{?with_kms:BuildRequires:	libdrm-devel}
# see dependency on libicu version below
BuildRequires:	libicu-devel < %{next_icu_abi}
BuildRequires:	libicu-devel >= %{icu_abi}
%{?with_libinput:BuildRequires:	libinput-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libxcb-devel >= 1.12
BuildRequires:	mtdev-devel
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	openssl-devel >= 1.1.1
%{?with_oci:BuildRequires:	oracle-instantclient-devel}
BuildRequires:	pcre2-16-devel >= 10.20
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_qm:BuildRequires:	qt5-linguist >= 5.2}
%{?with_doc:BuildRequires:	qt5-assistant >= 5.9}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	sed >= 4.0
%{?with_sqlite2:BuildRequires:	sqlite-devel}
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
%{?with_systemd:BuildRequires:	systemd-devel}
BuildRequires:	tar >= 1:1.22
%{?with_tslib:BuildRequires:	tslib-devel}
BuildRequires:	udev-devel
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.3.0}
BuildRequires:	wayland-devel
BuildRequires:	xcb-util-image-devel >= 0.3.9
BuildRequires:	xcb-util-keysyms-devel >= 0.3.9
BuildRequires:	xcb-util-renderutil-devel >= 0.3.9
BuildRequires:	xcb-util-wm-devel >= 0.3.9
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel >= 0.6
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.5.0
BuildRequires:	xorg-lib-libxkbcommon-x11-devel >= 0.5.0
BuildRequires:	xz
BuildRequires:	zlib-devel >= 1.0.8
BuildRequires:	zstd-devel >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		filterout	-flto

%define		qt5dir		%{_libdir}/qt5

%description
Qt is a software toolkit for developing applications.

This package contains base components, like Core, Network or Xml.

%description -l pl.UTF-8
Qt to programowy toolkit do tworzenia aplikacji.

Ten pakiet zawiera podstawowe komponenty, takie jak Core, Network czy
Xml.

%package -n Qt5AccessibilitySupport-devel
Summary:	Qt5 AccessibilitySupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 AccessibilitySupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	zlib-devel >= 1.0.8

%description -n Qt5AccessibilitySupport-devel
Qt5 AccessibilitySupport library - development files.

%description -n Qt5AccessibilitySupport-devel -l pl.UTF-8
Biblioteka Qt5 AccessibilitySupport - pliki programistyczne.

%package -n Qt5Bootstrap-devel
Summary:	Qt5 Bootstrap library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Bootstrap - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	zlib-devel >= 1.0.8

%description -n Qt5Bootstrap-devel
Qt5 Bootstrap library (minimal part of Qt5 Core) - development files.

%description -n Qt5Bootstrap-devel -l pl.UTF-8
Biblioteka Qt5 Bootstrap (minimalna część Qt5 Core) - pliki
programistyczne.

%package -n Qt5Concurrent
Summary:	Qt5 Concurrent library
Summary(pl.UTF-8):	Biblioteka Qt5 Concurrent
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}

%description -n Qt5Concurrent
The Qt5 Concurrent library provides high-level APIs that make it
possible to write multi-threaded programs without using low-level
threading primitives.

%description -n Qt5Concurrent -l pl.UTF-8
Biblioteka Qt5 Concurrent udostępnia wysokopoziomowe API umożliwiające
pisanie wielowątkowych programów bez wykorzystywania niskopoziomowych
elementów związanych z wątkami.

%package -n Qt5Concurrent-devel
Summary:	Qt5 Concurrent library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Concurrent - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Concurrent = %{version}-%{release}
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5Concurrent-devel
Header files for Qt5 Concurrent library.

%description -n Qt5Concurrent-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 Concurrent.

%package -n Qt5Core
Summary:	Qt5 Core library
Summary(pl.UTF-8):	Biblioteka Qt5 Core
Group:		Libraries
Requires:	pcre2-16 >= 10.20
Requires:	zlib >= 1.0.8
Requires:	zstd >= 1.3
Obsoletes:	qt5-qtbase < 5.2.0-1

%description -n Qt5Core
Qt5 Core library provides core non-GUI functionality.

%description -n Qt5Core -l pl.UTF-8
Biblioteka Qt5 Core zawiera podstawową funkcjonalność nie związaną z
graficznym interfejsem użytkownika (GUI).

%package -n Qt5Core-devel
Summary:	Qt5 Core library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Core - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core = %{version}-%{release}
Requires:	libicu-devel
Requires:	libstdc++-devel >= 6:4.7
Requires:	pcre2-16-devel >= 10.20
Requires:	qt5-build = %{version}-%{release}
Requires:	qt5-qmake = %{version}-%{release}
Requires:	zlib-devel >= 1.0.8
Obsoletes:	qt5-qtbase-devel < 5.2.0-1

%description -n Qt5Core-devel
Header files for Qt5 Core library.

%description -n Qt5Core-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 Core.

%package -n Qt5DBus
Summary:	Qt5 DBus library
Summary(pl.UTF-8):	Biblioteka Qt5 DBus
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}
Requires:	dbus-libs >= 1.2

%description -n Qt5DBus
The Qt5 D-Bus library is a Unix-only library that you can use to
perform Inter-Process Communication using the D-Bus protocol.

%description -n Qt5DBus -l pl.UTF-8
Biblioteka Qt5 D-Bus to wyłącznie uniksowa biblioteka pozwalająca na
komunikację międzyprocesową (IPC) przy użyciu protokołu D-Bus.

%package -n Qt5DBus-devel
Summary:	Qt5 DBus library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 DBus - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5DBus = %{version}-%{release}
Requires:	dbus-devel >= 1.2

%description -n Qt5DBus-devel
Header files for Qt5 DBus library.

%description -n Qt5DBus-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 DBus.

%package -n Qt5DeviceDiscoverySupport-devel
Summary:	Qt5 DeviceDiscoverySupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 DeviceDiscoverySupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5DeviceDiscoverySupport-devel
Qt5 DeviceDiscoverySupport library - development files.

%description -n Qt5DeviceDiscoverySupport-devel -l pl.UTF-8
Biblioteka Qt5 DeviceDiscoverySupport - pliki programistyczne.

%package -n Qt5EdidSupport-devel
Summary:	Qt5 EdidSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 EdidSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5EdidSupport-devel
Qt5 EdidSupport library - development files.

%description -n Qt5EdidSupport-devel -l pl.UTF-8
Biblioteka Qt5 EdidSupport - pliki programistyczne.

%package -n Qt5EglSupport-devel
Summary:	Qt5 EglSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 EglSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5EglSupport-devel
Qt5 EglSupport library - development files.

%description -n Qt5EglSupport-devel -l pl.UTF-8
Biblioteka Qt5 EglSupport - pliki programistyczne.

%package -n Qt5EventDispatcherSupport-devel
Summary:	Qt5 EventDispatcherSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 EventDispatcherSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	glib2-devel >= 2.0

%description -n Qt5EventDispatcherSupport-devel
Qt5 EventDispatcherSupport library - development files.

%description -n Qt5EventDispatcherSupport-devel -l pl.UTF-8
Biblioteka Qt5 EventDispatcherSupport - pliki programistyczne.

%package -n Qt5FbSupport-devel
Summary:	Qt5 FbSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 FbSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5FbSupport-devel
Qt5 FbSupport library - development files.

%description -n Qt5FbSupport-devel -l pl.UTF-8
Biblioteka Qt5 FbSupport - pliki programistyczne.

%package -n Qt5FontDatabaseSupport-devel
Summary:	Qt5 FontDatabaseSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 FontDatabaseSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5FontDatabaseSupport-devel
Qt5 FontDatabaseSupport library - development files.

%description -n Qt5FontDatabaseSupport-devel -l pl.UTF-8
Biblioteka Qt5 FontDatabaseSupport - pliki programistyczne.

%package -n Qt5GlxSupport-devel
Summary:	Qt5 GlxSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 GlxSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5GlxSupport-devel
Qt5 GlxSupport library - development files.

%description -n Qt5GlxSupport-devel -l pl.UTF-8
Biblioteka Qt5 GlxSupport - pliki programistyczne.

%package -n Qt5Gui
Summary:	Qt5 Gui library
Summary(pl.UTF-8):	Biblioteka Qt5 Gui
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}
# for ibus platforminputcontext plugin
Requires:	Qt5DBus = %{version}-%{release}
# for compose platforminputcontext plugin
Requires:	xorg-lib-libxkbcommon >= 0.4.1
Suggests:	Qt5Gui-platform-xcb

%description -n Qt5Gui
The Qt5 GUI library provides the basic enablers for graphical
applications written with Qt 5.

%description -n Qt5Gui -l pl
Biblioteka Qt5 Gui udostępnia podstawową funkcjonalność dla
graficznych aplikacji napisanych z użyciem Qt 5.

%package -n Qt5Gui-generic-libinput
Summary:	Qt5 Gui generic input plugin for libinput
Summary(pl.UTF-8):	Ogólna wtyczka wejścia Qt5 Gui z libinput
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}

%description -n Qt5Gui-generic-libinput
Qt5 Gui generic input plugin to get mouse, keyboard and touch events
via libinput.

%description -n Qt5Gui-generic-libinput -l pl.UTF-8
Ogólna wtyczka wejścia Qt5 Gui do pobierania zdarzeń myszy, klawiatury
i dotykowych poprzez libinput.

%package -n Qt5Gui-generic-tslib
Summary:	Qt5 Gui generic input plugin for TSlib (touchscreen panel events)
Summary(pl.UTF-8):	Ogólna wtyczka wejścia Qt5 Gui z TSlib (zdarzeń z paneli dotykowych)
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}

%description -n Qt5Gui-generic-tslib
Qt5 Gui generic input plugin for TSlib (touchscreen panel events).

%description -n Qt5Gui-generic-tslib -l pl.UTF-8
Ogólna wtyczka wejścia Qt5 Gui z TSlib (zdarzeń z paneli dotykowych).

%package -n Qt5Gui-generic-tuiotouch
Summary:	Qt5 Gui generic input plugin for TuioTouch
Summary(pl.UTF-8):	Ogólna wtyczka wejścia Qt5 Gui z TuioTouch
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}
Requires:	Qt5Network = %{version}-%{release}

%description -n Qt5Gui-generic-tuiotouch
Qt5 Gui generic input plugin for TuioTouch.

%description -n Qt5Gui-generic-tuiotouch -l pl.UTF-8
Ogólna wtyczka wejścia Qt5 Gui z TuioTouch.

%package -n Qt5Gui-platform-directfb
Summary:	Qt5 Gui platform plugin for DirectFB
Summary(pl.UTF-8):	Wtyczka platformy Qt5 Gui dla DirectFB
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}

%description -n Qt5Gui-platform-directfb
Qt5 Gui platform plugin for DirectFB.

%description -n Qt5Gui-platform-directfb -l pl.UTF-8
Wtyczka platformy Qt5 Gui dla DirectFB.

%package -n Qt5Gui-platform-egl
Summary:	Qt5 Gui platform plugin for minimal EGL
Summary(pl.UTF-8):	Wtyczka platformy Qt5 Gui dla minimalnego EGL
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}

%description -n Qt5Gui-platform-egl
Qt5 Gui platform plugin for minimal EGL.

%description -n Qt5Gui-platform-egl -l pl.UTF-8
Wtyczki platformy Qt5 Gui dla minimalnego EGL.

%package -n Qt5Gui-platform-eglfs
Summary:	Qt5 Gui platform plugin and library for EglFs integration layer
Summary(pl.UTF-8):	Wtyczka platformy Qt5 Gui oraz biblioteka warstwy integracyjnej EglFs
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}

%description -n Qt5Gui-platform-eglfs
Qt5 Gui platform plugin and library for EglFs integration layer.

%description -n Qt5Gui-platform-eglfs -l pl.UTF-8
Wtyczka platformy Qt5 Gui oraz biblioteka warstwy integracyjnej EglFs.

%package -n Qt5Gui-platform-eglfs-devel
Summary:	Development files for Qt5 EglFs integration layer
Summary(pl.UTF-8):	Pliki programistyczne warstwy integracyjnej Qt5 EglFs
Group:		Development/Libraries
Requires:	Qt5Gui-platform-eglfs = %{version}-%{release}

%description -n Qt5Gui-platform-eglfs-devel
Development files for Qt5 EglFs integration layer.

%description -n Qt5Gui-platform-eglfs-devel -l pl.UTF-8
Pliki programistyczne warstwy integracyjnej Qt5 EglFs.

%package -n Qt5Gui-platform-eglfs-kms
Summary:	Qt5 EglFs integration plugin for KMS
Summary(pl.UTF-8):	Wtyczka integracji Qt5 EglFs dla KMS
Group:		Libraries
Requires:	Qt5Gui-platform-eglfs = %{version}-%{release}
Obsoletes:	Qt5Gui-platform-kms < 5.5

%description -n Qt5Gui-platform-eglfs-kms
Qt5 EglFs integration plugin for KMS.

%description -n Qt5Gui-platform-eglfs-kms -l pl.UTF-8
Wtyczka integracji Qt5 EglFs dla KMS.

%package -n Qt5Gui-platform-eglfs-kms-devel
Summary:	Development files for Qt5 EglFs integration plugin for KMS
Summary(pl.UTF-8):	Pliki programistyczne dla wtyczki integracji Qt5 EglFs dla KMS
Group:		Libraries
Requires:	Qt5Gui-platform-eglfs = %{version}-%{release}
Obsoletes:	Qt5Gui-platform-kms < 5.5

%description -n Qt5Gui-platform-eglfs-kms-devel
Qt5 EglFs integration plugin for KMS - development files.

%description -n Qt5Gui-platform-eglfs-kms-devel -l pl.UTF-8
Wtyczka integracji Qt5 EglFs dla KMS - pliki programistyczne.

%package -n Qt5Gui-platform-eglfs-x11
Summary:	Qt5 EglFs integration plugin for X11
Summary(pl.UTF-8):	Wtyczka integracji Qt5 EglFs dla X11
Group:		Libraries
Requires:	Qt5Gui-platform-eglfs = %{version}-%{release}

%description -n Qt5Gui-platform-eglfs-x11
Qt5 EglFs integration plugin for X11.

%description -n Qt5Gui-platform-eglfs-x11 -l pl.UTF-8
Wtyczka integracji Qt5 EglFs dla X11.

%package -n Qt5Gui-platform-linuxfb
Summary:	Qt5 Gui platform plugin for Linux FrameBuffer
Summary(pl.UTF-8):	Wtyczka platformy Qt5 Gui dla linuksowego framebuffera
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}

%description -n Qt5Gui-platform-linuxfb
Qt5 Gui platform plugin for Linux FrameBuffer.

%description -n Qt5Gui-platform-linuxfb -l pl.UTF-8
Wtyczki platformy Qt5 Gui dla linuxksowego framebuffera.

%package -n Qt5Gui-platform-vnc
Summary:	Qt5 Gui platform plugin and library for VNC integration layer
Summary(pl.UTF-8):	Wtyczka platformy Qt5 Gui oraz biblioteka warstwy integracyjnej VNC
Group:		Libraries
Requires:	Qt5DBus = %{version}-%{release}
Requires:	Qt5Gui = %{version}-%{release}

%description -n Qt5Gui-platform-vnc
Qt5 Gui platform plugin and library for VNC integration layer.

%description -n Qt5Gui-platform-vnc -l pl.UTF-8
Wtyczka platformy Qt5 Gui oraz biblioteka warstwy integracyjnej VNC.

%package -n Qt5Gui-platform-vnc-devel
Summary:	Development files for Qt5 VNC integration layer
Summary(pl.UTF-8):	Pliki programistyczne warstwy integracyjnej Qt5 VNC
Group:		Development/Libraries

%description -n Qt5Gui-platform-vnc-devel
Development files for Qt5 VNC integration layer.

%description -n Qt5Gui-platform-vnc-devel -l pl.UTF-8
Pliki programistyczne warstwy integracyjnej Qt5 VNC.

%package -n Qt5Gui-platform-xcb
Summary:	Qt5 Gui platform plugin and library for XcbQpa integration layer
Summary(pl.UTF-8):	Wtyczka platformy Qt5 Gui oraz biblioteka warstwy integracyjnej XcbQpa
Group:		Libraries
Requires:	Qt5DBus = %{version}-%{release}
Requires:	Qt5Gui = %{version}-%{release}
Requires:	libxcb >= 1.10
Requires:	xorg-lib-libxkbcommon-x11 >= 0.4.1

%description -n Qt5Gui-platform-xcb
Qt5 Gui platform plugin and library for XcbQpa integration layer.

%description -n Qt5Gui-platform-xcb -l pl.UTF-8
Wtyczka platformy Qt5 Gui oraz biblioteka warstwy integracyjnej
XcbQpa.

%package -n Qt5Gui-platform-xcb-devel
Summary:	Development files for Qt5 XcbQpa integration layer
Summary(pl.UTF-8):	Pliki programistyczne warstwy integracyjnej Qt5 XcbQpa
Group:		Development/Libraries
Requires:	Qt5Gui-platform-eglfs = %{version}-%{release}

%description -n Qt5Gui-platform-xcb-devel
Development files for Qt5 XcbQpa integration layer.

%description -n Qt5Gui-platform-xcb-devel -l pl.UTF-8
Pliki programistyczne warstwy integracyjnej Qt5 XcbQpa.

%package -n Qt5Gui-platform-xcb-egl
Summary:	Qt5 XcbQpa integration plugin for EGL
Summary(pl.UTF-8):	Wtyczka integracji Qt5 XcbQpa dla EGL
Group:		Libraries
Requires:	Qt5Gui-platform-xcb = %{version}-%{release}

%description -n Qt5Gui-platform-xcb-egl
Qt5 XcbQpa integration plugin for EGL.

%description -n Qt5Gui-platform-xcb-egl -l pl.UTF-8
Wtyczka integracji Qt5 XcbQpa dla EGL.

%package -n Qt5Gui-platform-xcb-glx
Summary:	Qt5 XcbQpa integration plugin for GLX
Summary(pl.UTF-8):	Wtyczka integracji Qt5 XcbQpa dla GLX
Group:		Libraries
Requires:	Qt5Gui-platform-xcb = %{version}-%{release}

%description -n Qt5Gui-platform-xcb-glx
Qt5 XcbQpa integration plugin for GLX.

%description -n Qt5Gui-platform-xcb-glx -l pl.UTF-8
Wtyczka integracji Qt5 XcbQpa dla GLX.

%package -n Qt5Gui-platformtheme-gtk3
Summary:	Qt5 Gui platform theme plugin for GTK+ 3.x
Summary(pl.UTF-8):	Wtyczka motywów platform Qt5 Gui dla GTK+ 3.x
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}
Obsoletes:	Qt5Gui-platformtheme-gtk2 < 5.8

%description -n Qt5Gui-platformtheme-gtk3
Qt5 Gui platform theme plugin for GTK+ 3.x.

%description -n Qt5Gui-platformtheme-gtk3 -l pl.UTF-8
Wtyczka motywów platform Qt5 Gui dla GTK+ 3.x.

%package -n Qt5Gui-platformtheme-xdgdesktopportal
Summary:	Qt5 Gui platform theme plugin for xdg-desktop-portal
Summary(pl.UTF-8):	Wtyczka motywów platform Qt5 Gui dla xdg-desktop-portal
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}
Requires:	harfbuzz >= 1.6.0
Obsoletes:	Qt5Gui-platformtheme-flatpak < 5.12.1

%description -n Qt5Gui-platformtheme-xdgdesktopportal
Qt5 Gui platform theme plugin for xdg-desktop-portal.

%description -n Qt5Gui-platformtheme-xdgdesktopportal -l pl.UTF-8
Wtyczka motywów platform Qt5 Gui dla xdg-desktop-portal.

%package -n Qt5Gui-devel
Summary:	Qt5 Gui library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Gui - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Gui = %{version}-%{release}
Requires:	libpng-devel
Requires:	Vulkan-Loader-devel

%description -n Qt5Gui-devel
Header files for Qt5 Gui library.

%description -n Qt5Gui-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 Gui.

%package -n Qt5InputSupport-devel
Summary:	Qt5 InputSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 InputSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5InputSupport-devel
Qt5 InputSupport library - development files.

%description -n Qt5InputSupport-devel -l pl.UTF-8
Biblioteka Qt5 InputSupport - pliki programistyczne.

%package -n Qt5KmsSupport-devel
Summary:	Qt5 KmsSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 KmsSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5KmsSupport-devel
Qt5 KmsSupport library - development files.

%description -n Qt5KmsSupport-devel -l pl.UTF-8
Biblioteka Qt5 KmsSupport - pliki programistyczne.

%package -n Qt5Network
Summary:	Qt5 Network library
Summary(pl.UTF-8):	Biblioteka Qt5 Network
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}
# for bearer plugins (qconnman, qnm):
Requires:	Qt5DBus = %{version}-%{release}
%requires_ge_to openssl openssl-devel

%description -n Qt5Network
The Qt5 Network library provides classes to make network programming
easier and portable.

%description -n Qt5Network -l pl.UTF-8
Biblioteka Qt5 Network udostępnia klasy czyniące programowanie
sieciowe łatwiejszym i przenośnym.

%package -n Qt5Network-devel
Summary:	Qt5 Network library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Network - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Network = %{version}-%{release}
%requires_ge	openssl-devel

%description -n Qt5Network-devel
Header files for Qt5 Network library.

%description -n Qt5Network-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 Network.

%package -n Qt5OpenGL
Summary:	Qt5 OpenGL library
Summary(pl.UTF-8):	Biblioteka Qt5 OpenGL
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}
Requires:	Qt5Gui = %{version}-%{release}
Requires:	Qt5Widgets = %{version}-%{release}

%description -n Qt5OpenGL
The Qt5 OpenGL library offers classes that make it easy to use OpenGL
in Qt 5 applications.

%description -n Qt5OpenGL -l pl.UTF-8
Biblioteka Qt5 OpenGL oferuje klasy ułatwiające wykorzystywanie
OpenGL-a w aplikacjach Qt 5.

%package -n Qt5OpenGL-devel
Summary:	Qt5 OpenGL library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 OpenGL - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Gui-devel = %{version}-%{release}
Requires:	Qt5OpenGL = %{version}-%{release}
Requires:	Qt5Widgets-devel = %{version}-%{release}

%description -n Qt5OpenGL-devel
Header files for Qt5 OpenGL library.

%description -n Qt5OpenGL-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 OpenGL.

%package -n Qt5OpenGLExtensions-devel
Summary:	Qt5 OpenGLExtensions library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 OpenGLExtensions - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Gui-devel = %{version}-%{release}

%description -n Qt5OpenGLExtensions-devel
Qt5 OpenGLExtensions library (development files).

%description -n Qt5OpenGLExtensions-devel -l pl.UTF-8
Biblioteka Qt5 OpenGL Extensions - obsługa rozszerzeń OpenGL (pliki
programistyczne).

%package -n Qt5ServiceSupport-devel
Summary:	Qt5 ServiceSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 ServiceSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5ServiceSupport-devel
Qt5 ServiceSupport library - development files.

%description -n Qt5ServiceSupport-devel -l pl.UTF-8
Biblioteka Qt5 ServiceSupport - pliki programistyczne.

%package -n Qt5PlatformCompositorSupport-devel
Summary:	Qt5 PlatformCompositorSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 PlatformCompositorSupport - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5DBus-devel = %{version}-%{release}
Requires:	Qt5Gui-devel = %{version}-%{release}
Requires:	fontconfig-devel
Requires:	freetype-devel >= 2.2.0
Requires:	udev-devel
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXext-devel
Requires:	xorg-lib-libXrender-devel
Obsoletes:	Qt5PlatformSupport-devel < 5.8.0

%description -n Qt5PlatformCompositorSupport-devel
Qt5 PlatformCompositorSupport library (development files).

%description -n Qt5PlatformCompositorSupport-devel -l pl.UTF-8
Biblioteka Qt5 PlatformCompositorSupport - obsługa platformy (pliki
programistyczne).

%package -n Qt5PrintSupport
Summary:	Qt5 PrintSupport library
Summary(pl.UTF-8):	Biblioteka Qt5 PrintSupport
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}
Requires:	Qt5Gui = %{version}-%{release}
Requires:	Qt5Widgets = %{version}-%{release}
%{?with_cups:Requires:	cups-lib >= 1.4}

%description -n Qt5PrintSupport
The Qt5 PrintSupport library provides classes to make printing easier
and portable.

%description -n Qt5PrintSupport -l pl.UTF-8
Biblioteka Qt5 PrintSupport udostępnia klasy czyniące drukowanie
łatwiejszym i bardziej przenośnym.

%package -n Qt5PrintSupport-devel
Summary:	Qt5 PrintSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 PrintSupport - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Gui-devel = %{version}-%{release}
Requires:	Qt5PrintSupport = %{version}-%{release}
Requires:	Qt5Widgets-devel = %{version}-%{release}

%description -n Qt5PrintSupport-devel
Header files for Qt5 PrintSupport library.

%description -n Qt5PrintSupport-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 PrintSupport.

%package -n Qt5ThemeSupport-devel
Summary:	Qt5 ThemeSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 ThemeSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5ThemeSupport-devel
Qt5 ThemeSupport library - development files.

%description -n Qt5ThemeSupport-devel -l pl.UTF-8
Biblioteka Qt5 ThemeSupport - pliki programistyczne.

%package -n Qt5Sql
Summary:	Qt5 Sql library
Summary(pl.UTF-8):	Biblioteka Qt5 Sql
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}

%description -n Qt5Sql
The Qt5 Sql library provides a driver layer, SQL API layer, and a user
interface layer for SQL databases.

%description -n Qt5Sql -l pl.UTF-8
Biblioteka Qt5 Sql udostępnia warstwę sterowników, warstwę API SQL
oraz warstwę interfejsu użytkownika dla baz danych SQL.

%package -n Qt5Sql-devel
Summary:	Qt5 Sql library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Sql - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-devel
Header files for Qt5 Sql library.

%description -n Qt5Sql-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 Sql.

%package -n Qt5Sql-sqldriver-db2
Summary:	Qt5 Sql driver for IBM DB2 database
Summary(pl.UTF-8):	Sterownik Qt5 Sql dla bazy danych IBM DB2
Group:		Libraries
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-sqldriver-db2
Qt5 Sql driver for IBM DB2 database.

%description -n Qt5Sql-sqldriver-db2 -l pl.UTF-8
Sterownik Qt5 Sql dla bazy danych IBM DB2.

%package -n Qt5Sql-sqldriver-ibase
Summary:	Qt5 Sql driver for Firebird/InterBase database
Summary(pl.UTF-8):	Sterownik Qt5 Sql dla bazy danych Firebird/InterBase
Group:		Libraries
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-sqldriver-ibase
Qt5 Sql driver for Firebird/InterBase database.

%description -n Qt5Sql-sqldriver-ibase -l pl.UTF-8
Sterownik Qt5 Sql dla bazy danych Firebird/InterBase.

%package -n Qt5Sql-sqldriver-sqlite3
Summary:	Qt5 Sql driver for SQLite 3.x database
Summary(pl.UTF-8):	Sterownik Qt5 Sql dla bazy danych SQLite 3.x
Group:		Libraries
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-sqldriver-sqlite3
Qt5 Sql driver for SQLite 3.x database.

%description -n Qt5Sql-sqldriver-sqlite3 -l pl.UTF-8
Sterownik Qt5 Sql dla bazy danych SQLite 3.x.

%package -n Qt5Sql-sqldriver-sqlite2
Summary:	Qt5 Sql driver for SQLite 2.x database
Summary(pl.UTF-8):	Sterownik Qt5 Sql dla bazy danych SQLite 2.x
Group:		Libraries
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-sqldriver-sqlite2
Qt5 Sql driver for SQLite 2.x database.

%description -n Qt5Sql-sqldriver-sqlite2 -l pl.UTF-8
Sterownik Qt5 Sql dla bazy danych SQLite 2.x.

%package -n Qt5Sql-sqldriver-mysql
Summary:	Qt5 Sql driver for MySQL database
Summary(pl.UTF-8):	Sterownik Qt5 Sql dla bazy danych MySQL
Group:		Libraries
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-sqldriver-mysql
Qt5 Sql driver for MySQL database.

%description -n Qt5Sql-sqldriver-mysql -l pl.UTF-8
Sterownik Qt5 Sql dla bazy danych MySQL.

%package -n Qt5Sql-sqldriver-oci
Summary:	Qt5 Sql driver for Oracle database (using OCI interface)
Summary(pl.UTF-8):	Sterownik Qt5 Sql dla bazy danych Oracle (wykorzystujący interfejs OCI)
Group:		Libraries
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-sqldriver-oci
Qt5 Sql driver for Oracle database (using OCI interface).

%description -n Qt5Sql-sqldriver-oci -l pl.UTF-8
Sterownik Qt5 Sql dla bazy danych Oracle (wykorzystujący interfejs
OCI).

%package -n Qt5Sql-sqldriver-odbc
Summary:	Qt5 Sql driver for ODBC databases
Summary(pl.UTF-8):	Sterownik Qt5 Sql dla baz danych ODBC
Group:		Libraries
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-sqldriver-odbc
Qt5 Sql driver for ODBC databases.

%description -n Qt5Sql-sqldriver-odbc -l pl.UTF-8
Sterownik Qt5 Sql dla baz danych ODBC.

%package -n Qt5Sql-sqldriver-pgsql
Summary:	Qt5 Sql driver for PostgreSQL database
Summary(pl.UTF-8):	Sterownik Qt5 Sql dla bazy danych PostgreSQL
Group:		Libraries
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-sqldriver-pgsql
Qt5 Sql driver for PostgreSQL database.

%description -n Qt5Sql-sqldriver-pgsql -l pl.UTF-8
Sterownik Qt5 Sql dla bazy danych PostgreSQL.

%package -n Qt5Sql-sqldriver-tds
Summary:	Qt5 Sql driver for Sybase/MS SQL database (using TDS interface)
Summary(pl.UTF-8):	Sterownik Qt5 Sql dla bazy danych Sybase/MS SQL (wykorzystujący interfejs TDS)
Group:		Libraries
Requires:	Qt5Sql = %{version}-%{release}

%description -n Qt5Sql-sqldriver-tds
Qt5 Sql driver for Sybase/MS SQL database (using TDS interface).

%description -n Qt5Sql-sqldriver-tds -l pl.UTF-8
Sterownik Qt5 Sql dla bazy danych Sybase/MS SQL (wykorzystujący
interfejs TDS).

%package -n Qt5Test
Summary:	Qt5 Test library
Summary(pl.UTF-8):	Biblioteka Qt5 Test
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}

%description -n Qt5Test
The Qt5 Test library provides classes for unit testing Qt 5
applications and libraries.

%description -n Qt5Test -l pl.UTF-8
Biblioteka Qt5 Test udostępnia klasy do testów jednostkowych aplikacji
oraz bibliotek Qt 5.

%package -n Qt5Test-devel
Summary:	Qt5 Test library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Test - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Test = %{version}-%{release}

%description -n Qt5Test-devel
Header files for Qt5 Test library.

%description -n Qt5Test-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 Test.

%package -n Qt5VulkanSupport-devel
Summary:	Qt5 VulkanSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 VulkanSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5VulkanSupport-devel
Qt5 VulkanSupport library - development files.

%description -n Qt5VulkanSupport-devel -l pl.UTF-8
Biblioteka Qt5 VulkanSupport - pliki programistyczne.

%package -n Qt5Widgets
Summary:	Qt5 Widgets library
Summary(pl.UTF-8):	Biblioteka Qt5 Widgets
Group:		X11/Libraries
Requires:	Qt5Core = %{version}-%{release}
Requires:	Qt5Gui = %{version}-%{release}

%description -n Qt5Widgets
The Qt5 Widgets library extends Qt 5 GUI with C++ widget
functionality.

%description -n Qt5Widgets -l pl.UTF-8
Biblioteka Qt5 Widgets rozszerza graficzny interfejs Qt 5 o
funkcjonalność widgetów C++.

%package -n Qt5Widgets-devel
Summary:	Qt5 Widgets library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Widgets - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Gui-devel = %{version}-%{release}
Requires:	Qt5Widgets = %{version}-%{release}
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXext-devel

%description -n Qt5Widgets-devel
Header files for Qt5 Widgets library.

%description -n Qt5Widgets-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 Widgets.

%package -n Qt5XkbCommonSupport-devel
Summary:	Qt5 XkbCommonSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 XkbCommonSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}

%description -n Qt5XkbCommonSupport-devel
Qt5 XkbCommonSupport library - development files.

%description -n Qt5XkbCommonSupport-devel -l pl.UTF-8
Biblioteka Qt5 XkbCommonSupport - pliki programistyczne.

%package -n Qt5Xml
Summary:	Qt5 Xml library
Summary(pl.UTF-8):	Biblioteka Qt5 Xml
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}

%description -n Qt5Xml
The Qt5 Xml library provides C++ implementations of the SAX and DOM
standards for XML.

%description -n Qt5Xml -l pl.UTF-8
Biblioteka Qt5 Xml udostępnia implementację w C++ standardów SAX oraz
DOM dla formatu XML.

%package -n Qt5Xml-devel
Summary:	Qt5 Xml library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Xml - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Xml = %{version}-%{release}

%description -n Qt5Xml-devel
Header files for Qt5 Xml library.

%description -n Qt5Xml-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 Xml.

%package -n qt5-doc-common
Summary:	Common part of Qt5 documentation
Summary(pl.UTF-8):	Część wspólna dokumentacji do Qt5
Group:		Documentation
BuildArch:	noarch

%description -n qt5-doc-common
Common part of Qt5 documentation, global for all components.

%description -n qt5-doc-common -l pl.UTF-8
Część wspólna dokumentacji do Qt5 ("global", dla wszystkich
elementów).

%package doc
Summary:	Qt5 application framework base components documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja podstawowych komponentów szkieletu aplikacji Qt5 w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common = %{version}-%{release}
BuildArch:	noarch

%description doc
Qt5 application framework base components documentation in HTML
format.

%description doc -l pl.UTF-8
Dokumentacja podstawowych komponentów szkieletu aplikacji Qt5 w
formacie HTML.

%package doc-qch
Summary:	Qt5 application framework base components documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja podstawowych komponentów szkieletu aplikacji Qt5 w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common = %{version}-%{release}
BuildArch:	noarch

%description doc-qch
Qt5 application framework base components documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja podstawowych komponentów szkieletu aplikacji Qt5 w
formacie QCH.

%package examples
Summary:	Examples for Qt5 application framework base components
Summary(pl.UTF-8):	Przykłady do podstawowych komponentów szkieletu aplikacji Qt5
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Examples for Qt5 application framework base components.

%description examples -l pl.UTF-8
Przykłady do podstawowych komponentów szkieletu aplikacji Qt5.

%package -n qt5-build
Summary:	Qt5 build tools
Summary(pl.UTF-8):	Narzędzia do budowania dla Qt5
Group:		Development/Tools

%description -n qt5-build
This package includes the Qt resource compiler (rcc), meta objects
compiler (moc), user interface compiler (uic) etc.

%description -n qt5-build -l pl.UTF-8
Ten pakiet zawiera kompilator zasobów Qt (rcc), kompilator
metaobiektów (moc), kompilator interfejsów użytkownika (uic) i podobne
narzędzia.

%package -n qt5-qmake
Summary:	Qt5 makefile generator
Summary(pl.UTF-8):	Generator plików makefile dla aplikacji Qt5
Group:		Development/Tools

%description -n qt5-qmake
Qt5 makefile generator.

%description -n qt5-qmake -l pl.UTF-8
Generator plików makefile dla aplikacji Qt5.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version} %{?with_qm:-a1}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i -e 's,usr/X11R6/,usr/,g' mkspecs/linux-g++-64/qmake.conf

# change QMAKE FLAGS to build
%{__sed} -i -e '
	s|^\(QMAKE_CC *\)=.*gcc|\1= %{__cc}|;
	s|^\(QMAKE_CXX *\)=.*g++|\1= %{__cxx}|;
	s|^QMAKE_CFLAGS_RELEASE_WITH_DEBUGINFO .*|QMAKE_CFLAGS_RELEASE_WITH_DEBUGINFO += -g %{rpmcppflags} %{rpmcflags}|;
	s|^QMAKE_CXXFLAGS_RELEASE_WITH_DEBUGINFO .*|QMAKE_CXXFLAGS_RELEASE_WITH_DEBUGINFO += -g %{rpmcppflags} %{rpmcxxflags}|;
	' mkspecs/common/g++-base.conf
%{__sed} -i -e '
	s|^\(QMAKE_CFLAGS_RELEASE *\)+=.*|\1+= %{rpmcppflags} %{rpmcflags}|;
	s|^\(QMAKE_CXXFLAGS_RELEASE *\)+=.*|\1+= %{rpmcppflags} %{rpmcxxflags}|;
	s|^\(QMAKE_CFLAGS_DEBUG *\)+=.*|\1+= %{debugcflags}|;
	s|^\(QMAKE_CXXFLAGS_DEBUG *\)+=.*|\1+= %{debugcflags}|;
	s|^\(QMAKE_LFLAGS *\)+=.*|\1+= %{rpmldflags}|;
	' mkspecs/common/gcc-base.conf

# define QMAKE_STRIP to true, so we get useful -debuginfo pkgs
%{__sed} -i -e '
	s|^\(QMAKE_STRIP *\)=.*|\1= :|;
	' mkspecs/common/linux.conf

%{__sed} -i -e '1{
	s,^#!.*bin/python$,#!%{__python3},
	s,^#!.*bin/env perl,#!%{__perl},
}' \
	bin/fixqt4headers.pl \
	bin/syncqt.pl \
	mkspecs/features/uikit/devices.py

%build
# pass OPTFLAGS to build qmake itself with optimization
export OPTFLAGS="%{rpmcflags}"
export PATH=$PWD/bin:$PATH

# DEFAULT OPTIONS FOR ALL BUILDS
COMMONOPT=" \
	-confirm-license \
	-opensource \
	-verbose \
	%{?debug:-debug} \
	%{!?debug:-release} \
	-prefix %{qt5dir} \
	-bindir %{qt5dir}/bin \
	-docdir %{_docdir}/qt5-doc \
	-headerdir %{_includedir}/qt5 \
	-libdir %{_libdir} \
	-plugindir %{qt5dir}/plugins \
	-datadir %{_datadir}/qt5 \
	-sysconfdir %{_sysconfdir}/qt5 \
	-examplesdir %{_examplesdir}/qt5 \
%if %{with mysql}
	-I/usr/include/mysql \
%endif
%if %{with pgsql}
	-I/usr/include/postgresql/server \
%endif
	-%{!?with_cups:no-}cups \
	-%{!?with_directfb:no-}directfb \
	-dbus-linked \
	-fontconfig \
	-glib \
	-%{!?with_gtk:no-}gtk \
	-icu \
	%{?with_systemd:-journald} \
	-no-compile-examples \
	%{!?with_egl:-no-eglfs} \
	%{!?with_statx:-no-feature-statx} \
	%{!?with_kms:-no-kms} \
	%{!?with_libinput:-no-libinput} \
	-no-rpath \
	-no-separate-debug-info \
	%{!?with_sse2:-no-sse2} \
	%{!?with_sse3:-no-sse3} \
	%{!?with_ssse3:-no-ssse3} \
	%{!?with_sse41:-no-sse4.1} \
	%{!?with_sse42:-no-sse4.2} \
	%{!?with_avx:-no-avx} \
	%{!?with_avx2:-no-avx2} \
	-no-use-gold-linker \
	-openssl-linked \
	-optimized-qmake \
	-%{!?with_pch:no-}pch \
	%{?with_red_reloc:-reduce-relocations} \
	-sm \
	-system-doubleconversion \
	-system-freetype \
	-system-harfbuzz \
	-system-libjpeg \
	-system-libpng \
	-system-pcre \
	-system-sqlite \
	-system-zlib \
	%{?with_tslib:-tslib} \
	-xcb \
	-xkbcommon \
	%{!?with_db2:-no}-sql-db2 \
	%{!?with_ibase:-no}-sql-ibase \
	%{!?with_mysql:-no}-sql-mysql \
	%{!?with_oci:-no}-sql-oci \
	%{!?with_odbc:-no}-sql-odbc \
	%{!?with_pgsql:-no}-sql-psql \
	%{!?with_sqlite2:-no}-sql-sqlite2 \
	%{!?with_sqlite3:-no}-sql-sqlite \
	%{!?with_freetds:-no}-sql-tds \
"

# STATIC
%if %{with static_libs}
./configure $COMMONOPT -static

%{__make} -C src
if [ ! -d staticlib ]; then
	mkdir staticlib
	cp -a lib/*.a staticlib
fi
%{__make} distclean
%endif

# SHARED
./configure $COMMONOPT -shared

%{__make}
%if %{with doc}
# use just built qdoc instead of requiring already installed qt5-build
wd="$(pwd)"
%{__sed} -i -e 's|%{qt5dir}/bin/qdoc|LD_LIBRARY_PATH='${wd}'/lib$${LD_LIBRARY_PATH:+:$$LD_LIBRARY_PATH} '${wd}'/bin/qdoc|' src/*/Makefile
%{__make} docs
%endif

%if %{with qm}
export QMAKEPATH=$(pwd)
cd qttranslations-everywhere-src-%{version}
../bin/qmake
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/qt5,%{_bindir},%{_pkgconfigdir},%{qt5dir}/libexec}

# for QtSolutions (qtlockedfile, qtsingleapplication, etc)
install -d $RPM_BUILD_ROOT%{_includedir}/qt5/QtSolutions

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

%if %{with qm}
%{__make} -C qttranslations-everywhere-src-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
# keep only qt and qtbase
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt5/translations/{assistant,designer,linguist,qt_help,qtconnectivity,qtdeclarative,qtlocation,qtmultimedia,qtquickcontrols,qtquickcontrols2,qtscript,qtserialport,qtwebengine,qtwebsockets,qtxmlpatterns}_*.qm
%else
install -d $RPM_BUILD_ROOT%{_datadir}/qt5/translations
%endif

# external plugins loaded from qtbase libs
install -d $RPM_BUILD_ROOT%{qt5dir}/plugins/iconengines

# kill unnecessary -L%{_libdir} from *.la, *.prl, *.pc
%{__sed} -i -e "s,-L%{_libdir} \?,,g" \
	$RPM_BUILD_ROOT%{_libdir}/*.{la,prl} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# symlinks in system bin dir
cd $RPM_BUILD_ROOT%{_bindir}
ln -sf ../%{_lib}/qt5/bin/moc moc-qt5
ln -sf ../%{_lib}/qt5/bin/qmake qmake-qt5
ln -sf ../%{_lib}/qt5/bin/uic uic-qt5
ln -sf ../%{_lib}/qt5/bin/rcc rcc-qt5
ln -sf ../%{_lib}/qt5/bin/qdbuscpp2xml qdbuscpp2xml-qt5
ln -sf ../%{_lib}/qt5/bin/qdbusxml2cpp qdbusxml2cpp-qt5
ln -sf ../%{_lib}/qt5/bin/qdoc qdoc-qt5
ln -sf ../%{_lib}/qt5/bin/qlalr qlalr-qt5
cd -

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/corelib
ifecho_tree examples %{_examplesdir}/qt5/dbus
ifecho_tree examples %{_examplesdir}/qt5/gui
ifecho_tree examples %{_examplesdir}/qt5/network
ifecho_tree examples %{_examplesdir}/qt5/opengl
ifecho_tree examples %{_examplesdir}/qt5/qpa
ifecho_tree examples %{_examplesdir}/qt5/qtconcurrent
ifecho_tree examples %{_examplesdir}/qt5/qtestlib
ifecho_tree examples %{_examplesdir}/qt5/sql
ifecho_tree examples %{_examplesdir}/qt5/vulkan
ifecho_tree examples %{_examplesdir}/qt5/widgets
ifecho_tree examples %{_examplesdir}/qt5/xml

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_localedir}/*/LC_MESSAGES layout
find_qt5_qm()
{
	name="$1"
	find $RPM_BUILD_ROOT%{_datadir}/qt5/translations -name "${name}_*.qm" | \
		sed -e "s:^$RPM_BUILD_ROOT::" \
		    -e 's:\(.*/'$name'_\)\([a-z][a-z][a-z]\?\)\(_[A-Z][A-Z]\)\?\(\.qm\)$:%lang(\2\3) \1\2\3\4:'
}

echo '%defattr(644,root,root,755)' > qtbase.lang
%if %{with qm}
find_qt5_qm qt >> qtbase.lang
find_qt5_qm qtbase >> qtbase.lang
%endif

install -d $RPM_BUILD_ROOT%{qt5dir}/plugins/styles

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Concurrent -p /sbin/ldconfig
%postun	-n Qt5Concurrent -p /sbin/ldconfig

%post	-n Qt5Core -p /sbin/ldconfig
%postun	-n Qt5Core -p /sbin/ldconfig

%post	-n Qt5DBus -p /sbin/ldconfig
%postun	-n Qt5DBus -p /sbin/ldconfig

%post	-n Qt5Gui -p /sbin/ldconfig
%postun	-n Qt5Gui -p /sbin/ldconfig

%post	-n Qt5Gui-platform-eglfs -p /sbin/ldconfig
%postun	-n Qt5Gui-platform-eglfs -p /sbin/ldconfig

%post	-n Qt5Gui-platform-eglfs-kms -p /sbin/ldconfig
%postun	-n Qt5Gui-platform-eglfs-kms -p /sbin/ldconfig

%post	-n Qt5Gui-platform-xcb -p /sbin/ldconfig
%postun	-n Qt5Gui-platform-xcb -p /sbin/ldconfig

%post	-n Qt5Network -p /sbin/ldconfig
%postun	-n Qt5Network -p /sbin/ldconfig

%post	-n Qt5OpenGL -p /sbin/ldconfig
%postun	-n Qt5OpenGL -p /sbin/ldconfig

%post	-n Qt5PrintSupport -p /sbin/ldconfig
%postun	-n Qt5PrintSupport -p /sbin/ldconfig

%post	-n Qt5Sql -p /sbin/ldconfig
%postun	-n Qt5Sql -p /sbin/ldconfig

%post	-n Qt5Test -p /sbin/ldconfig
%postun	-n Qt5Test -p /sbin/ldconfig

%post	-n Qt5Widgets -p /sbin/ldconfig
%postun	-n Qt5Widgets -p /sbin/ldconfig

%post	-n Qt5Xml -p /sbin/ldconfig
%postun	-n Qt5Xml -p /sbin/ldconfig

%files -n Qt5AccessibilitySupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtAccessibilitySupport
%{_includedir}/qt5/QtLinuxAccessibilitySupport
%{_libdir}/libQt5AccessibilitySupport.a
%{_libdir}/libQt5AccessibilitySupport.prl
%{_libdir}/libQt5LinuxAccessibilitySupport.a
%{_libdir}/libQt5LinuxAccessibilitySupport.prl
%{_libdir}/cmake/Qt5AccessibilitySupport
%{_libdir}/cmake/Qt5LinuxAccessibilitySupport
%{qt5dir}/mkspecs/modules/qt_lib_accessibility_support_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_linuxaccessibility_support_private.pri

%files -n Qt5Bootstrap-devel
%defattr(644,root,root,755)
# static-only
%{_libdir}/libQt5Bootstrap.a
%{_libdir}/libQt5Bootstrap.prl
%{qt5dir}/mkspecs/modules/qt_lib_bootstrap_private.pri

%files -n Qt5Concurrent
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Concurrent.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Concurrent.so.5

%files -n Qt5Concurrent-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Concurrent.so
%{_libdir}/libQt5Concurrent.prl
%{_includedir}/qt5/QtConcurrent
%{_pkgconfigdir}/Qt5Concurrent.pc
%{_libdir}/cmake/Qt5Concurrent
%{qt5dir}/mkspecs/modules/qt_lib_concurrent.pri
%{qt5dir}/mkspecs/modules/qt_lib_concurrent_private.pri

%files -n Qt5Core -f qtbase.lang
%defattr(644,root,root,755)
%doc dist/{README,changes-*}
%attr(755,root,root) %{_libdir}/libQt5Core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Core.so.5
%dir %{_sysconfdir}/qt5
%dir %{qt5dir}
%dir %{qt5dir}/bin
%dir %{qt5dir}/libexec
%dir %{qt5dir}/mkspecs
%dir %{qt5dir}/mkspecs/modules
%dir %{qt5dir}/plugins
%dir %{_datadir}/qt5
%dir %{_datadir}/qt5/translations

%files -n Qt5Core-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Core.so
%{_libdir}/libQt5Core.prl
%dir %{_libdir}/metatypes
%{_libdir}/metatypes/qt5core_metatypes.json
%dir %{_includedir}/qt5
%dir %{_includedir}/qt5/QtSolutions
%{_includedir}/qt5/QtCore
%{_pkgconfigdir}/Qt5Core.pc
%{_libdir}/cmake/Qt5
%{_libdir}/cmake/Qt5Core
%{qt5dir}/mkspecs/modules/qt_lib_core.pri
%{qt5dir}/mkspecs/modules/qt_lib_core_private.pri
%attr(755,root,root) %{qt5dir}/bin/tracegen

%files -n Qt5DBus
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5DBus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5DBus.so.5

%files -n Qt5DBus-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5DBus.so
%{_libdir}/libQt5DBus.prl
%{_includedir}/qt5/QtDBus
%{_pkgconfigdir}/Qt5DBus.pc
%{_libdir}/cmake/Qt5DBus
%{qt5dir}/mkspecs/modules/qt_lib_dbus.pri
%{qt5dir}/mkspecs/modules/qt_lib_dbus_private.pri

%files -n Qt5DeviceDiscoverySupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtDeviceDiscoverySupport
%{_libdir}/libQt5DeviceDiscoverySupport.a
%{_libdir}/libQt5DeviceDiscoverySupport.prl
%{_libdir}/cmake/Qt5DeviceDiscoverySupport
%{qt5dir}/mkspecs/modules/qt_lib_devicediscovery_support_private.pri

%files -n Qt5EdidSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtEdidSupport
%{_libdir}/libQt5EdidSupport.a
%{_libdir}/libQt5EdidSupport.prl
%{_libdir}/cmake/Qt5EdidSupport
%{qt5dir}/mkspecs/modules/qt_lib_edid_support_private.pri

%files -n Qt5EglSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtEglSupport
%{_libdir}/libQt5EglSupport.a
%{_libdir}/libQt5EglSupport.prl
%{_libdir}/cmake/Qt5EglSupport
%{qt5dir}/mkspecs/modules/qt_lib_egl_support_private.pri

%files -n Qt5EventDispatcherSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtEventDispatcherSupport
%{_libdir}/libQt5EventDispatcherSupport.a
%{_libdir}/libQt5EventDispatcherSupport.prl
%{_libdir}/cmake/Qt5EventDispatcherSupport
%{qt5dir}/mkspecs/modules/qt_lib_eventdispatcher_support_private.pri

%files -n Qt5FbSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtFbSupport
%{_libdir}/libQt5FbSupport.a
%{_libdir}/libQt5FbSupport.prl
%{_libdir}/cmake/Qt5FbSupport
%{qt5dir}/mkspecs/modules/qt_lib_fb_support_private.pri

%files -n Qt5FontDatabaseSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtFontDatabaseSupport
%{_libdir}/libQt5FontDatabaseSupport.a
%{_libdir}/libQt5FontDatabaseSupport.prl
%{_libdir}/cmake/Qt5FontDatabaseSupport
%{qt5dir}/mkspecs/modules/qt_lib_fontdatabase_support_private.pri

%files -n Qt5GlxSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtGlxSupport
%{_libdir}/libQt5GlxSupport.a
%{_libdir}/libQt5GlxSupport.prl
%{_libdir}/cmake/Qt5GlxSupport
%{qt5dir}/mkspecs/modules/qt_lib_glx_support_private.pri

%files -n Qt5Gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Gui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Gui.so.5
# loaded from src/gui/kernel/qgenericpluginfactory.cpp
%dir %{qt5dir}/plugins/generic
# R: udev-libs (by all qevdev* plugins)
%attr(755,root,root) %{qt5dir}/plugins/generic/libqevdevkeyboardplugin.so
%attr(755,root,root) %{qt5dir}/plugins/generic/libqevdevmouseplugin.so
%attr(755,root,root) %{qt5dir}/plugins/generic/libqevdevtabletplugin.so
%attr(755,root,root) %{qt5dir}/plugins/generic/libqevdevtouchplugin.so
# loaded from src/gui/image/qicon.cpp
%dir %{qt5dir}/plugins/iconengines
# loaded from src/gui/image/qimage{reader,writer}.cpp
%dir %{qt5dir}/plugins/imageformats
%attr(755,root,root) %{qt5dir}/plugins/imageformats/libqgif.so
%attr(755,root,root) %{qt5dir}/plugins/imageformats/libqico.so
# R: libjpeg
%attr(755,root,root) %{qt5dir}/plugins/imageformats/libqjpeg.so
# loaded from src/gui/kernel/qplatforminputcontextfactory.cpp
%dir %{qt5dir}/plugins/platforminputcontexts
# R: libxkbcommon
%attr(755,root,root) %{qt5dir}/plugins/platforminputcontexts/libcomposeplatforminputcontextplugin.so
# R: Qt5DBus
%attr(755,root,root) %{qt5dir}/plugins/platforminputcontexts/libibusplatforminputcontextplugin.so
# loaded from src/gui/kernel/qplatformintegrationfactory.cpp
%dir %{qt5dir}/plugins/platforms
# R: fontconfig freetype
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqminimal.so
# R: OpenGL freetype libX11 libXrender
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqoffscreen.so
# loaded from src/gui/kernel/qplatformthemefactory.cpp
%dir %{qt5dir}/plugins/platformthemes
# common for base -devel and plugin-specific files
%dir %{_libdir}/cmake/Qt5Gui

%if %{with libinput}
%files -n Qt5Gui-generic-libinput
%defattr(644,root,root,755)
# R: libinput libxkbcommon udev
%attr(755,root,root) %{qt5dir}/plugins/generic/libqlibinputplugin.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QLibInputPlugin.cmake
%endif

%if %{with tslib}
%files -n Qt5Gui-generic-tslib
%defattr(644,root,root,755)
# R: tslib
%attr(755,root,root) %{qt5dir}/plugins/generic/libqtslibplugin.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QTsLibPlugin.cmake
%endif

%files -n Qt5Gui-generic-tuiotouch
%defattr(644,root,root,755)
# R: Qt5Network
%attr(755,root,root) %{qt5dir}/plugins/generic/libqtuiotouchplugin.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QTuioTouchPlugin.cmake

%if %{with directfb}
%files -n Qt5Gui-platform-directfb
%defattr(644,root,root,755)
# R: DirectFB fontconfig freetype
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqdirectfb.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QDirectFbIntegrationPlugin.cmake
%endif

%if %{with egl}
%files -n Qt5Gui-platform-egl
%defattr(644,root,root,755)
# R: egl fontconfig freetype
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqminimalegl.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalEglIntegrationPlugin.cmake
%endif

%files -n Qt5Gui-platform-eglfs
%defattr(644,root,root,755)
# R: Qt5Gui Qt5Core EGL GL ts fontconfig freetype glib2 udev mtdev
%attr(755,root,root) %{_libdir}/libQt5EglFSDeviceIntegration.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5EglFSDeviceIntegration.so.5
# R: egl fontconfig freetype (for two following)
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqeglfs.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSIntegrationPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSEmulatorIntegrationPlugin.cmake
# loaded from src/plugins/platforms/eglfs/qeglfsdeviceintegration.cpp
%dir %{qt5dir}/plugins/egldeviceintegrations
%attr(755,root,root) %{qt5dir}/plugins/egldeviceintegrations/libqeglfs-emu-integration.so

%files -n Qt5Gui-platform-eglfs-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtEglFSDeviceIntegration
%attr(755,root,root) %{_libdir}/libQt5EglFSDeviceIntegration.so
%{_libdir}/cmake/Qt5EglFSDeviceIntegration
%{_libdir}/libQt5EglFSDeviceIntegration.prl
%{qt5dir}/mkspecs/modules/qt_lib_eglfsdeviceintegration_private.pri

%if %{with kms}
%files -n Qt5Gui-platform-eglfs-kms
%defattr(644,root,root,755)
# R: gl egl libdrm libgbm udev
%attr(755,root,root) %{_libdir}/libQt5EglFsKmsSupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5EglFsKmsSupport.so.5
%attr(755,root,root) %{qt5dir}/plugins/egldeviceintegrations/libqeglfs-kms-integration.so
%attr(755,root,root) %{qt5dir}/plugins/egldeviceintegrations/libqeglfs-kms-egldevice-integration.so

%files -n Qt5Gui-platform-eglfs-kms-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5EglFsKmsSupport.so
%{_libdir}/libQt5EglFsKmsSupport.prl
%{_libdir}/cmake/Qt5EglFsKmsSupport
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsEglDeviceIntegrationPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsGbmIntegrationPlugin.cmake
%{qt5dir}/mkspecs/modules/qt_lib_eglfs_kms_support_private.pri
%endif

%files -n Qt5Gui-platform-eglfs-x11
%defattr(644,root,root,755)
# R: libX11 libxcb
%attr(755,root,root) %{qt5dir}/plugins/egldeviceintegrations/libqeglfs-x11-integration.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSX11IntegrationPlugin.cmake

%files -n Qt5Gui-platform-linuxfb
%defattr(644,root,root,755)
# R: fontconfig freetype libinput tslib udev-libs
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqlinuxfb.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QLinuxFbIntegrationPlugin.cmake

%files -n Qt5Gui-platform-vnc
%defattr(644,root,root,755)
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqvnc.so

%files -n Qt5Gui-platform-vnc-devel
%defattr(644,root,root,755)
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QVncIntegrationPlugin.cmake

%files -n Qt5Gui-platform-xcb
%defattr(644,root,root,755)
# R: Qt5DBus xorg* xcb* libxkbcommon-x11 fontconfig freetype
%attr(755,root,root) %{_libdir}/libQt5XcbQpa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5XcbQpa.so.5
# R: Qt5DBus xcb-* xorg*
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqxcb.so
# loaded from src/plugins/platforms/xcb/gl_integrations/qxcbglintegrationfactory.cpp
%dir %{qt5dir}/plugins/xcbglintegrations
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbIntegrationPlugin.cmake

%files -n Qt5Gui-platform-xcb-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5XcbQpa.so
%{_libdir}/libQt5XcbQpa.prl
%{_libdir}/cmake/Qt5XcbQpa
%{qt5dir}/mkspecs/modules/qt_lib_xcb_qpa_lib_private.pri

%files -n Qt5Gui-platform-xcb-egl
%defattr(644,root,root,755)
%attr(755,root,root) %{qt5dir}/plugins/xcbglintegrations/libqxcb-egl-integration.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbEglIntegrationPlugin.cmake

%files -n Qt5Gui-platform-xcb-glx
%defattr(644,root,root,755)
%attr(755,root,root) %{qt5dir}/plugins/xcbglintegrations/libqxcb-glx-integration.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbGlxIntegrationPlugin.cmake

%if %{with gtk}
%files -n Qt5Gui-platformtheme-gtk3
%defattr(644,root,root,755)
# R: gtk+3
%attr(755,root,root) %{qt5dir}/plugins/platformthemes/libqgtk3.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QGtk3ThemePlugin.cmake
%endif

%files -n Qt5Gui-platformtheme-xdgdesktopportal
%defattr(644,root,root,755)
%attr(755,root,root) %{qt5dir}/plugins/platformthemes/libqxdgdesktopportal.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QXdgDesktopPortalThemePlugin.cmake

%files -n Qt5Gui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{qt5dir}/bin/qvkgen
%attr(755,root,root) %{_libdir}/libQt5Gui.so
%{_libdir}/libQt5Gui.prl
%{_libdir}/metatypes/qt5gui_metatypes.json
%{_includedir}/qt5/QtGui
%{_includedir}/qt5/QtPlatformHeaders
%{_pkgconfigdir}/Qt5Gui.pc
%{_libdir}/cmake/Qt5Gui/Qt5GuiConfig*.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevKeyboardPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevMousePlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTabletPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTouchScreenPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QGifPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QICOPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QJpegPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QComposePlatformInputContextPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QIbusPlatformInputContextPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalIntegrationPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QOffscreenIntegrationPlugin.cmake
%{qt5dir}/mkspecs/modules/qt_lib_gui.pri
%{qt5dir}/mkspecs/modules/qt_lib_gui_private.pri

%files -n Qt5InputSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtInputSupport
%{_libdir}/libQt5InputSupport.a
%{_libdir}/libQt5InputSupport.prl
%{_libdir}/cmake/Qt5InputSupport
%{qt5dir}/mkspecs/modules/qt_lib_input_support_private.pri

%files -n Qt5KmsSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtKmsSupport
%{_libdir}/libQt5KmsSupport.a
%{_libdir}/libQt5KmsSupport.prl
%{_libdir}/cmake/Qt5KmsSupport
%{qt5dir}/mkspecs/modules/qt_lib_kms_support_private.pri

%files -n Qt5Network
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Network.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Network.so.5
# loaded from src/network/bearer/qnetworkconfigmanager_p.cpp
%dir %{qt5dir}/plugins/bearer
# R: Qt5DBus
%attr(755,root,root) %{qt5dir}/plugins/bearer/libqconnmanbearer.so
%attr(755,root,root) %{qt5dir}/plugins/bearer/libqgenericbearer.so
# R: Qt5DBus
%attr(755,root,root) %{qt5dir}/plugins/bearer/libqnmbearer.so

%files -n Qt5Network-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Network.so
%{_libdir}/libQt5Network.prl
%{_includedir}/qt5/QtNetwork
%{_pkgconfigdir}/Qt5Network.pc
%dir %{_libdir}/cmake/Qt5Network
%{_libdir}/cmake/Qt5Network/Qt5NetworkConfig*.cmake
%{_libdir}/cmake/Qt5Network/Qt5Network_QConnmanEnginePlugin.cmake
%{_libdir}/cmake/Qt5Network/Qt5Network_QGenericEnginePlugin.cmake
%{_libdir}/cmake/Qt5Network/Qt5Network_QNetworkManagerEnginePlugin.cmake
%{qt5dir}/mkspecs/modules/qt_lib_network.pri
%{qt5dir}/mkspecs/modules/qt_lib_network_private.pri

%files -n Qt5OpenGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5OpenGL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5OpenGL.so.5

%files -n Qt5OpenGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5OpenGL.so
%{_libdir}/libQt5OpenGL.prl
%{_includedir}/qt5/QtOpenGL
%{_pkgconfigdir}/Qt5OpenGL.pc
%{_libdir}/cmake/Qt5OpenGL
%{qt5dir}/mkspecs/modules/qt_lib_opengl.pri
%{qt5dir}/mkspecs/modules/qt_lib_opengl_private.pri

%files -n Qt5OpenGLExtensions-devel
%defattr(644,root,root,755)
# static-only
%{_libdir}/libQt5OpenGLExtensions.a
%{_libdir}/libQt5OpenGLExtensions.prl
%{_includedir}/qt5/QtOpenGLExtensions
%{_pkgconfigdir}/Qt5OpenGLExtensions.pc
%{_libdir}/cmake/Qt5OpenGLExtensions
%{qt5dir}/mkspecs/modules/qt_lib_openglextensions.pri
%{qt5dir}/mkspecs/modules/qt_lib_openglextensions_private.pri

%files -n Qt5PlatformCompositorSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtPlatformCompositorSupport
%{_libdir}/libQt5PlatformCompositorSupport.a
%{_libdir}/libQt5PlatformCompositorSupport.prl
%{_libdir}/cmake/Qt5PlatformCompositorSupport
%{qt5dir}/mkspecs/modules/qt_lib_platformcompositor_support_private.pri

%files -n Qt5PrintSupport
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5PrintSupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5PrintSupport.so.5
# loaded from src/printsupport/kernel/qplatformprintplugin.cpp
%dir %{qt5dir}/plugins/printsupport
%if %{with cups}
%attr(755,root,root) %{qt5dir}/plugins/printsupport/libcupsprintersupport.so
%endif

%files -n Qt5PrintSupport-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5PrintSupport.so
%{_libdir}/libQt5PrintSupport.prl
%{_includedir}/qt5/QtPrintSupport
%{_pkgconfigdir}/Qt5PrintSupport.pc
%dir %{_libdir}/cmake/Qt5PrintSupport
%{_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupportConfig*.cmake
%if %{with cups}
%{_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupport_QCupsPrinterSupportPlugin.cmake
%endif
%{qt5dir}/mkspecs/modules/qt_lib_printsupport.pri
%{qt5dir}/mkspecs/modules/qt_lib_printsupport_private.pri

%files -n Qt5ServiceSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtServiceSupport
%{_libdir}/libQt5ServiceSupport.a
%{_libdir}/libQt5ServiceSupport.prl
%{_libdir}/cmake/Qt5ServiceSupport
%{qt5dir}/mkspecs/modules/qt_lib_service_support_private.pri

%files -n Qt5Sql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Sql.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Sql.so.5
# loaded from src/sql/kernel/qsqldatabase.cpp
%dir %{qt5dir}/plugins/sqldrivers
# common for base -devel and plugin-specific files
%dir %{_libdir}/cmake/Qt5Sql

%if %{with db2}
%files -n Qt5Sql-sqldriver-db2
%defattr(644,root,root,755)
# R: (proprietary) DB2 libs
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqldb2.so
%{_libdir}/cmake/Qt5Sql/Qt5Sql_QDB2DriverPlugin.cmake
%endif

%if %{with ibase}
%files -n Qt5Sql-sqldriver-ibase
%defattr(644,root,root,755)
# R: Firebird-lib
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlibase.so
%{_libdir}/cmake/Qt5Sql/Qt5Sql_QIBaseDriverPlugin.cmake
%endif

%if %{with sqlite3}
%files -n Qt5Sql-sqldriver-sqlite3
%defattr(644,root,root,755)
# R: sqlite3
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlite.so
%{_libdir}/cmake/Qt5Sql/Qt5Sql_QSQLiteDriverPlugin.cmake
%endif

%if %{with sqlite2}
%files -n Qt5Sql-sqldriver-sqlite2
%defattr(644,root,root,755)
# R: sqlite >= 2
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlite2.so
%{_libdir}/cmake/Qt5Sql/Qt5Sql_QSQLite2DriverPlugin.cmake
%endif

%if %{with mysql}
%files -n Qt5Sql-sqldriver-mysql
%defattr(644,root,root,755)
# R: mysql-libs
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlmysql.so
%{_libdir}/cmake/Qt5Sql/Qt5Sql_QMYSQLDriverPlugin.cmake
%endif

%if %{with oci}
%files -n Qt5Sql-sqldriver-oci
%defattr(644,root,root,755)
# R: (proprietary) Oracle libs
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqloci.so
%{_libdir}/cmake/Qt5Sql/Qt5Sql_QOCIDriverPlugin.cmake
%endif

%if %{with odbc}
%files -n Qt5Sql-sqldriver-odbc
%defattr(644,root,root,755)
# R: unixODBC
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlodbc.so
%{_libdir}/cmake/Qt5Sql/Qt5Sql_QODBCDriverPlugin.cmake
%endif

%if %{with pgsql}
%files -n Qt5Sql-sqldriver-pgsql
%defattr(644,root,root,755)
# R: postgresql-libs
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqlpsql.so
%{_libdir}/cmake/Qt5Sql/Qt5Sql_QPSQLDriverPlugin.cmake
%endif

%if %{with freetds}
%files -n Qt5Sql-sqldriver-tds
%defattr(644,root,root,755)
# R: freetds
%attr(755,root,root) %{qt5dir}/plugins/sqldrivers/libqsqltds.so
%{_libdir}/cmake/Qt5Sql/Qt5Sql_QTDSDriverPlugin.cmake
%endif

%files -n Qt5Sql-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Sql.so
%{_libdir}/libQt5Sql.prl
%{_includedir}/qt5/QtSql
%{_pkgconfigdir}/Qt5Sql.pc
%{_libdir}/cmake/Qt5Sql/Qt5SqlConfig*.cmake
%{qt5dir}/mkspecs/modules/qt_lib_sql.pri
%{qt5dir}/mkspecs/modules/qt_lib_sql_private.pri

%files -n Qt5Test
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Test.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Test.so.5

%files -n Qt5Test-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Test.so
%{_libdir}/libQt5Test.prl
%{_includedir}/qt5/QtTest
%{_pkgconfigdir}/Qt5Test.pc
%{_libdir}/cmake/Qt5Test
%{qt5dir}/mkspecs/modules/qt_lib_testlib.pri
%{qt5dir}/mkspecs/modules/qt_lib_testlib_private.pri

%files -n Qt5ThemeSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtThemeSupport
%{_libdir}/libQt5ThemeSupport.a
%{_libdir}/libQt5ThemeSupport.prl
%{_libdir}/cmake/Qt5ThemeSupport
%{qt5dir}/mkspecs/modules/qt_lib_theme_support_private.pri

%files -n Qt5VulkanSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtVulkanSupport
%{_libdir}/libQt5VulkanSupport.a
%{_libdir}/libQt5VulkanSupport.prl
%{_libdir}/cmake/Qt5VulkanSupport
%{qt5dir}/mkspecs/modules/qt_lib_vulkan_support_private.pri

%files -n Qt5Widgets
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Widgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Widgets.so.5
%dir %{qt5dir}/plugins/styles

%files -n Qt5Widgets-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Widgets.so
%{_libdir}/libQt5Widgets.prl
%{_libdir}/metatypes/qt5widgets_metatypes.json
%{_includedir}/qt5/QtWidgets
%{_pkgconfigdir}/Qt5Widgets.pc
%dir %{_libdir}/cmake/Qt5Widgets
%{_libdir}/cmake/Qt5Widgets/Qt5WidgetsConfig*.cmake
%{_libdir}/cmake/Qt5Widgets/Qt5WidgetsMacros.cmake
%{qt5dir}/mkspecs/modules/qt_lib_widgets.pri
%{qt5dir}/mkspecs/modules/qt_lib_widgets_private.pri

%files -n Qt5XkbCommonSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtXkbCommonSupport
%{_libdir}/libQt5XkbCommonSupport.a
%{_libdir}/libQt5XkbCommonSupport.prl
%{_libdir}/cmake/Qt5XkbCommonSupport
%{qt5dir}/mkspecs/modules/qt_lib_xkbcommon_support_private.pri

%files -n Qt5Xml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Xml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Xml.so.5

%files -n Qt5Xml-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Xml.so
%{_libdir}/libQt5Xml.prl
%{_includedir}/qt5/QtXml
%{_pkgconfigdir}/Qt5Xml.pc
%{_libdir}/cmake/Qt5Xml
%{qt5dir}/mkspecs/modules/qt_lib_xml.pri
%{qt5dir}/mkspecs/modules/qt_lib_xml_private.pri

%files -n qt5-doc-common
%defattr(644,root,root,755)
%dir %{_docdir}/qt5-doc
%{_docdir}/qt5-doc/config
%{_docdir}/qt5-doc/global

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qmake
%{_docdir}/qt5-doc/qtconcurrent
%{_docdir}/qt5-doc/qtcore
%{_docdir}/qt5-doc/qtdbus
%{_docdir}/qt5-doc/qtgui
%{_docdir}/qt5-doc/qtnetwork
%{_docdir}/qt5-doc/qtopengl
%{_docdir}/qt5-doc/qtplatformheaders
%{_docdir}/qt5-doc/qtprintsupport
%{_docdir}/qt5-doc/qtsql
%{_docdir}/qt5-doc/qttestlib
%{_docdir}/qt5-doc/qtwidgets
%{_docdir}/qt5-doc/qtxml

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qmake.qch
%{_docdir}/qt5-doc/qtconcurrent.qch
%{_docdir}/qt5-doc/qtcore.qch
%{_docdir}/qt5-doc/qtdbus.qch
%{_docdir}/qt5-doc/qtgui.qch
%{_docdir}/qt5-doc/qtnetwork.qch
%{_docdir}/qt5-doc/qtopengl.qch
%{_docdir}/qt5-doc/qtplatformheaders.qch
%{_docdir}/qt5-doc/qtprintsupport.qch
%{_docdir}/qt5-doc/qtsql.qch
%{_docdir}/qt5-doc/qttestlib.qch
%{_docdir}/qt5-doc/qtwidgets.qch
%{_docdir}/qt5-doc/qtxml.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
%dir %{_examplesdir}/qt5
%doc %{_examplesdir}/qt5/README
%{_examplesdir}/qt5/examples.pro

%files -n qt5-build
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/moc-qt5
%attr(755,root,root) %{_bindir}/qdbuscpp2xml-qt5
%attr(755,root,root) %{_bindir}/qdbusxml2cpp-qt5
%attr(755,root,root) %{_bindir}/qdoc-qt5
%attr(755,root,root) %{_bindir}/qlalr-qt5
%attr(755,root,root) %{_bindir}/rcc-qt5
%attr(755,root,root) %{_bindir}/uic-qt5
%attr(755,root,root) %{qt5dir}/bin/fixqt4headers.pl
%attr(755,root,root) %{qt5dir}/bin/moc
%attr(755,root,root) %{qt5dir}/bin/qdbuscpp2xml
%attr(755,root,root) %{qt5dir}/bin/qdbusxml2cpp
%attr(755,root,root) %{qt5dir}/bin/qlalr
%attr(755,root,root) %{qt5dir}/bin/rcc
%attr(755,root,root) %{qt5dir}/bin/syncqt.pl
%attr(755,root,root) %{qt5dir}/bin/uic

%files -n qt5-qmake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qmake-qt5
%attr(755,root,root) %{qt5dir}/bin/qmake
%{qt5dir}/mkspecs/aix-*
%{qt5dir}/mkspecs/android-*
%{qt5dir}/mkspecs/common
%{qt5dir}/mkspecs/dummy
%{qt5dir}/mkspecs/cygwin-*
%{qt5dir}/mkspecs/darwin-*
%{qt5dir}/mkspecs/devices
%{qt5dir}/mkspecs/features
%{qt5dir}/mkspecs/freebsd-*
%{qt5dir}/mkspecs/haiku-*
%{qt5dir}/mkspecs/hpuxi-*
%{qt5dir}/mkspecs/hurd-*
%{qt5dir}/mkspecs/integrity-armv7*
%{qt5dir}/mkspecs/integrity-armv8*
%{qt5dir}/mkspecs/integrity-x86
%{qt5dir}/mkspecs/linux-*
%{qt5dir}/mkspecs/lynxos-*
%{qt5dir}/mkspecs/macx-*
%{qt5dir}/mkspecs/netbsd-*
%{qt5dir}/mkspecs/openbsd-*
%{qt5dir}/mkspecs/qnx-*
%{qt5dir}/mkspecs/solaris-*
%{qt5dir}/mkspecs/unsupported
%{qt5dir}/mkspecs/wasm-emscripten
%{qt5dir}/mkspecs/win32-*
%{qt5dir}/mkspecs/winrt-*
%{qt5dir}/mkspecs/*.pri
