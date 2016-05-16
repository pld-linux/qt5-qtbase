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
%bcond_without	qch		# QCH documentation
%bcond_without	qm		# QM translations
# -- features
%bcond_without	cups		# CUPS printing support
%bcond_without	directfb	# DirectFB platform support
%bcond_without	egl		# EGL (EGLFS, minimal EGL) platform support
%bcond_without	gtk		# GTK+ theme integration
%bcond_without	kms		# KMS platform support
%bcond_without	libinput	# libinput support
%bcond_without	pch		# pch (pre-compiled headers) in qmake
%bcond_with	systemd		# logging to journald
%bcond_without	tslib		# tslib support
%bcond_with	openvg		# OpenVG support
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

%if %{with bootstrap}
%undefine	with_qch
%undefine	with_qm
%endif

%define		icu_abi		57
%define		next_icu_abi	%(echo $((%{icu_abi} + 1)))

%define		orgname		qtbase
Summary:	Qt5 - base components
Summary(pl.UTF-8):	Biblioteka Qt5 - podstawowe komponenty
Name:		qt5-%{orgname}
Version:	5.5.1
Release:	6
# See LGPL_EXCEPTION.txt for exception details
License:	LGPL v2 with Digia Qt LGPL Exception v1.1 or GPL v3
Group:		X11/Libraries
Source0:	http://download.qt.io/official_releases/qt/5.5/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	687e2b122fa2c3390b5e20a166d38038
Source1:	http://download.qt.io/official_releases/qt/5.5/%{version}/submodules/qttranslations-opensource-src-%{version}.tar.xz
# Source1-md5:	1f89d53fe759db123b4b6d9de9d9e8c9
Patch0:		qtbase-oracle-instantclient.patch
Patch1:		%{name}-system_cacerts.patch
URL:		http://www.qt.io/
%{?with_directfb:BuildRequires:	DirectFB-devel}
BuildRequires:	EGL-devel
%{?with_ibase:BuildRequires:	Firebird-devel}
%{?with_openvg:BuildRequires:	Mesa-libOpenVG-devel}
%{?with_kms:BuildRequires:	Mesa-libgbm-devel}
BuildRequires:	OpenGL-devel
%{?with_kms:BuildRequires:	OpenGLESv2-devel}
BuildRequires:	alsa-lib-devel
%{?with_gtk:BuildRequires:	atk-devel}
%{?with_cups:BuildRequires:	cups-devel >= 1.4}
BuildRequires:	dbus-devel >= 1.2
BuildRequires:	fontconfig-devel
%{?with_freetds:BuildRequires:	freetds-devel}
BuildRequires:	freetype-devel >= 2.1.3
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	gdb
BuildRequires:	glib2-devel >= 2.0.0
%{?with_gtk:BuildRequires:	gtk+2-devel >= 2:2.18}
%{?with_kms:BuildRequires:	libdrm-devel}
# see dependency on libicu version below
BuildRequires:	libicu-devel < %{next_icu_abi}
BuildRequires:	libicu-devel >= %{icu_abi}
%{?with_libinput:BuildRequires:	libinput-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel
BuildRequires:	libxcb-devel >= 1.10
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	openssl-devel
%{?with_oci:BuildRequires:	oracle-instantclient-devel}
BuildRequires:	pcre16-devel >= 8.30
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-backend-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	pulseaudio-devel >= 0.9.10
%{?with_qch:BuildRequires:	qt5-assistant >= 5.2}
%{?with_qm:BuildRequires:	qt5-linguist >= 5.2}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	sed >= 4.0
%{?with_sqlite2:BuildRequires:	sqlite-devel}
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
%{?with_systemd:BuildRequires:	systemd-devel}
BuildRequires:	tar >= 1:1.22
%{?with_tslib:BuildRequires:	tslib-devel}
BuildRequires:	udev-devel
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.3.0}
BuildRequires:	xcb-util-image-devel
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xcb-util-renderutil-devel
BuildRequires:	xcb-util-wm-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.4.1
BuildRequires:	xorg-lib-libxkbcommon-x11-devel >= 0.4.1
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%define		qt5dir		%{_libdir}/qt5

%description
Qt is a software toolkit for developing applications.

This package contains base components, like Core, Network or Xml.

%description -l pl.UTF-8
Qt to programowy toolkit do tworzenia aplikacji.

Ten pakiet zawiera podstawowe komponenty, takie jak Core, Network czy
Xml.

%package -n Qt5Bootstrap-devel
Summary:	Qt5 Bootstrap library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Bootstrap - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt5Core headers
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	zlib-devel

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
Requires:	pcre16 >= 8.30
Obsoletes:	qt5-qtbase

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
Requires:	glib2-devel >= 2.0
Requires:	libicu-devel
Requires:	pcre16-devel >= 8.30
Requires:	zlib-devel
Obsoletes:	qt5-qtbase-devel

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

%package -n Qt5Gui
Summary:	Qt5 Gui library
Summary(pl.UTF-8):	Biblioteka Qt5 Gui
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}
# for ibus platforminputcontext plugin
Requires:	Qt5DBus = %{version}-%{release}
# for compose platforminputcontext plugin
Requires:	xorg-lib-libxkbcommon >= 0.4.1

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

%package -n Qt5Gui-platform-eglfs-x11
Summary:	Qt5 EglFs integration plugin for X11
Summary(pl.UTF-8):	Wtyczka integracji Qt5 EglFs dla X11
Group:		Libraries
Requires:	Qt5Gui-platform-eglfs = %{version}-%{release}

%description -n Qt5Gui-platform-eglfs-x11
Qt5 EglFs integration plugin for X11.

%description -n Qt5Gui-platform-eglfs-x11 -l pl.UTF-8
Wtyczka integracji Qt5 EglFs dla X11.

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

%package -n Qt5Gui-platformtheme-gtk2
Summary:	Qt5 Gui platform theme plugin for GTK+ 2.x
Summary(pl.UTF-8):	Wtyczka motywów platform Qt5 Gui dla GTK+ 2.x
Group:		Libraries
Requires:	Qt5Gui = %{version}-%{release}

%description -n Qt5Gui-platformtheme-gtk2
Qt5 Gui platform theme plugin for GTK+ 2.x.

%description -n Qt5Gui-platformtheme-gtk2 -l pl.UTF-8
Wtyczka motywów platform Qt5 Gui dla GTK+ 2.x.

%package -n Qt5Gui-devel
Summary:	Qt5 Gui library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Gui - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5Gui = %{version}-%{release}
Requires:	libpng-devel

%description -n Qt5Gui-devel
Header files for Qt5 Gui library.

%description -n Qt5Gui-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 Gui.

%package -n Qt5Network
Summary:	Qt5 Network library
Summary(pl.UTF-8):	Biblioteka Qt5 Network
Group:		Libraries
Requires:	Qt5Core = %{version}-%{release}
# for bearer plugins (qconnman, qnm):
Requires:	Qt5DBus = %{version}-%{release}
%requires_ge_to	openssl	openssl-devel

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
Requires:	openssl-devel

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

%package -n Qt5PlatformSupport-devel
Summary:	Qt5 PlatformSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 PlatformSupport - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel = %{version}-%{release}
Requires:	Qt5DBus-devel = %{version}-%{release}
Requires:	Qt5Gui-devel = %{version}-%{release}
Requires:	fontconfig-devel
Requires:	freetype-devel >= 2.1.3
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXrender-devel
Requires:	xorg-lib-libXext-devel
Requires:	udev-devel

%description -n Qt5PlatformSupport-devel
Qt5 PlatformSupport library (development files).

%description -n Qt5OpenGLExtensions-devel -l pl.UTF-8
Biblioteka Qt5 PlatformSupport - obsługa platformy (pliki
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n qt5-doc-common
Common part of Qt5 documentation, global for all components.

%description -n qt5-doc-common -l pl.UTF-8
Część wspólna dokumentacji do Qt5 ("global", dla wszystkich
elementów).

%package doc
Summary:	HTML documentation for Qt5 application framework base components
Summary(pl.UTF-8):	Dokumentacja HTML do podstawowych komponentów szkieletu aplikacji Qt5
Group:		Documentation
Requires:	qt5-doc-common = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
HTML documentation for Qt5 application framework base components.

%description doc -l pl.UTF-8
Dokumentacja HTML do podstawowych komponentów szkieletu aplikacji Qt5.

%package doc-qch
Summary:	QCH documentation for Qt5 application framework base components
Summary(pl.UTF-8):	Dokumentacja QCH do podstawowych komponentów szkieletu aplikacji Qt5
Group:		Documentation
Requires:	qt5-doc-common = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
QCH documentation for Qt5 application framework base components.

%description doc-qch -l pl.UTF-8
Dokumentacja QCH do podstawowych komponentów szkieletu aplikacji Qt5.

%package examples
Summary:	Examples for Qt5 application framework base components
Summary(pl.UTF-8):	Przykłady do podstawowych komponentów szkieletu aplikacji Qt5
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
%setup -q -n %{orgname}-opensource-src-%{version} %{?with_qm:-a1}
%patch0 -p1
%patch1 -p1

%{__sed} -i -e 's,usr/X11R6/,usr/,g' mkspecs/linux-g++-64/qmake.conf

# change QMAKE FLAGS to build
%{__sed} -i -e '
	s|^\(QMAKE_COMPILER *\)=.*gcc|\1= %{__cc}|;
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
	-gstreamer 1.0 \
	-%{!?with_gtk:no-}gtkstyle \
	-iconv \
	-icu \
	%{?with_systemd:-journald} \
	-largefile \
	-nis \
	%{!?with_egl:-no-eglfs} \
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
	-openssl-linked \
	-optimized-qmake \
	-%{!?with_pch:no-}pch \
	-reduce-relocations \
	-sm \
	-system-freetype \
	-system-libjpeg \
	-system-libpng \
	-system-pcre \
	-system-sqlite \
	-system-xcb \
	-system-xkbcommon \
	-system-zlib \
	%{?with_tslib:-tslib} \
	-%{!?with_openvg:no-}openvg \
	-xcursor \
	-xfixes \
	-xinerama \
	-xinput2 \
	-xkb \
	-xrandr \
	-xrender \
	-xshape"

# STATIC
%if %{with static_libs}
OPT=" \
	--sql-db2=%{?with_db2:qt}%{!?with_db2:no} \
	--sql-ibase=%{?with_ibase:qt}%{!?with_ibase:no} \
	--sql-mysql=%{?with_mysql:qt}%{!?with_mysql:no} \
	--sql-oci=%{?with_oci:qt}%{!?with_oci:no} \
	--sql-odbc=%{?with_odbc:qt}%{!?with_odbc:no} \
	--sql-psql=%{?with_pgsql:qt}%{!?with_pgsql:no} \
	--sql-sqlite2=%{?with_sqlite2:qt}%{!?with_sqlite2:no} \
	--sql-sqlite=%{?with_sqlite3:qt}%{!?with_sqlite3:no} \
	--sql-tds=%{?with_freetds:qt}%{!?with_freetds:no} \
	-static"

./configure $COMMONOPT $OPT

%{__make} -C src
if [ ! -d staticlib ]; then
	mkdir staticlib
	cp -a lib/*.a staticlib
fi
%{__make} distclean
%endif

# SHARED
OPT=" \
	--sql-db2=%{?with_db2:plugin}%{!?with_db2:no} \
	--sql-ibase=%{?with_ibase:plugin}%{!?with_ibase:no} \
	--sql-mysql=%{?with_mysql:plugin}%{!?with_mysql:no} \
	--sql-oci=%{?with_oci:plugin}%{!?with_oci:no} \
	--sql-odbc=%{?with_odbc:plugin}%{!?with_odbc:no} \
	--sql-psql=%{?with_pgsql:plugin}%{!?with_pgsql:no} \
	--sql-sqlite2=%{?with_sqlite2:plugin}%{!?with_sqlite2:no} \
	--sql-sqlite=%{?with_sqlite3:plugin}%{!?with_sqlite3:no} \
	--sql-tds=%{?with_freetds:plugin}%{!?with_freetds:no} \
	-shared"

./configure $COMMONOPT $OPT

%{__make}

# use just built qdoc instead of requiring already installed qt5-build
wd="$(pwd)"
%{__sed} -i -e 's|%{qt5dir}/bin/qdoc|LD_LIBRARY_PATH='${wd}'/lib$${LD_LIBRARY_PATH:+:$$LD_LIBRARY_PATH} '${wd}'/bin/qdoc|' src/*/Makefile qmake/Makefile.qmake-docs
# build only HTML docs if without qch (which require qhelpgenerator)
%{__make} %{!?with_qch:html_}docs

%if %{with qm}
export QMAKEPATH=$(pwd)
cd qttranslations-opensource-src-%{version}
../bin/qmake
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/qt5,%{_bindir},%{_pkgconfigdir}}

# for QtSolutions (qtlockedfile, qtsingleapplication, etc)
install -d $RPM_BUILD_ROOT%{_includedir}/qt5/QtSolutions

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_%{!?with_qch:html_}docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with qm}
%{__make} -C qttranslations-opensource-src-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
# keep only qt and qtbase
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt5/translations/{assistant,designer,linguist,qmlviewer,qt_help,qtconfig,qtconnectivity,qtdeclarative,qtlocation,qtmultimedia,qtquick1,qtquickcontrols,qtscript,qtwebsockets,qtxmlpatterns}_*.qm
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
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.?
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
ifecho_tree examples %{_examplesdir}/qt5/touch
ifecho_tree examples %{_examplesdir}/qt5/widgets
ifecho_tree examples %{_examplesdir}/qt5/xml

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_datadir}/locale/*/LC_MESSAGES layout
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

%files -n Qt5Bootstrap-devel
%defattr(644,root,root,755)
# static-only
%{_libdir}/libQt5Bootstrap.a
%{_libdir}/libQt5Bootstrap.prl
%{_pkgconfigdir}/Qt5Bootstrap.pc
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
%doc LGPL_EXCEPTION.txt header.* dist/{README,changes-*}
%attr(755,root,root) %{_libdir}/libQt5Core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Core.so.5
%dir /etc/qt5
%dir %{qt5dir}
%dir %{qt5dir}/bin
%dir %{qt5dir}/mkspecs
%dir %{qt5dir}/mkspecs/modules
%dir %{qt5dir}/plugins
%dir %{_datadir}/qt5
%dir %{_datadir}/qt5/translations

%files -n Qt5Core-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Core.so
%{_libdir}/libQt5Core.prl
%dir %{_includedir}/qt5
%dir %{_includedir}/qt5/QtSolutions
%{_includedir}/qt5/QtCore
%{_pkgconfigdir}/Qt5Core.pc
%{_libdir}/cmake/Qt5
%{_libdir}/cmake/Qt5Core
%{qt5dir}/mkspecs/modules/qt_lib_core.pri
%{qt5dir}/mkspecs/modules/qt_lib_core_private.pri

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
# R: fontconfig freetype udev-libs
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqlinuxfb.so
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqminimal.so
# R: freetype libX11 libXrender
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
%attr(755,root,root) %{_libdir}/libQt5EglDeviceIntegration.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5EglDeviceIntegration.so.5
# R: egl fontconfig freetype (for two following)
%attr(755,root,root) %{qt5dir}/plugins/platforms/libqeglfs.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSIntegrationPlugin.cmake
# loaded from src/plugins/platforms/eglfs/qeglfsdeviceintegration.cpp
%dir %{qt5dir}/plugins/egldeviceintegrations

%files -n Qt5Gui-platform-eglfs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5EglDeviceIntegration.so
%{_libdir}/libQt5EglDeviceIntegration.prl
%{_pkgconfigdir}/Qt5EglDeviceIntegration.pc
%{qt5dir}/mkspecs/modules/qt_lib_eglfs_device_lib_private.pri

%if %{with kms}
%files -n Qt5Gui-platform-eglfs-kms
%defattr(644,root,root,755)
# R: gl egl libdrm libgbm udev
%attr(755,root,root) %{qt5dir}/plugins/egldeviceintegrations/libqeglfs-kms-integration.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsIntegrationPlugin.cmake
%endif

%files -n Qt5Gui-platform-eglfs-x11
%defattr(644,root,root,755)
# R: libX11 libxcb
%attr(755,root,root) %{qt5dir}/plugins/egldeviceintegrations/libqeglfs-x11-integration.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSX11IntegrationPlugin.cmake

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
%{_pkgconfigdir}/Qt5XcbQpa.pc
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
%files -n Qt5Gui-platformtheme-gtk2
%defattr(644,root,root,755)
# R: gtk+2
%attr(755,root,root) %{qt5dir}/plugins/platformthemes/libqgtk2.so
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QGtk2ThemePlugin.cmake
%endif

%files -n Qt5Gui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Gui.so
%{_libdir}/libQt5Gui.prl
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
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QLinuxFbIntegrationPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalIntegrationPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QOffscreenIntegrationPlugin.cmake
%{qt5dir}/mkspecs/modules/qt_lib_gui.pri
%{qt5dir}/mkspecs/modules/qt_lib_gui_private.pri

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

%files -n Qt5PlatformSupport-devel
%defattr(644,root,root,755)
# static-only
%{_libdir}/libQt5PlatformSupport.a
%{_libdir}/libQt5PlatformSupport.prl
%{_includedir}/qt5/QtPlatformSupport
%{_pkgconfigdir}/Qt5PlatformSupport.pc
%{qt5dir}/mkspecs/modules/qt_lib_platformsupport_private.pri

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

%files -n Qt5Widgets
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Widgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Widgets.so.5

%files -n Qt5Widgets-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Widgets.so
%{_libdir}/libQt5Widgets.prl
%{_includedir}/qt5/QtWidgets
%{_pkgconfigdir}/Qt5Widgets.pc
%dir %{_libdir}/cmake/Qt5Widgets
%{_libdir}/cmake/Qt5Widgets/Qt5WidgetsConfig*.cmake
%{_libdir}/cmake/Qt5Widgets/Qt5WidgetsMacros.cmake
%{qt5dir}/mkspecs/modules/qt_lib_widgets.pri
%{qt5dir}/mkspecs/modules/qt_lib_widgets_private.pri

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
%{_docdir}/qt5-doc/global

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qdoc
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

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qdoc.qch
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
%attr(755,root,root) %{qt5dir}/bin/moc
%attr(755,root,root) %{qt5dir}/bin/qdbuscpp2xml
%attr(755,root,root) %{qt5dir}/bin/qdbusxml2cpp
%attr(755,root,root) %{qt5dir}/bin/qdoc
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
%{qt5dir}/mkspecs/blackberry-*
%{qt5dir}/mkspecs/common
%{qt5dir}/mkspecs/cygwin-*
%{qt5dir}/mkspecs/darwin-*
%{qt5dir}/mkspecs/devices
%{qt5dir}/mkspecs/features
%{qt5dir}/mkspecs/freebsd-*
%{qt5dir}/mkspecs/haiku-*
%{qt5dir}/mkspecs/hpux-*
%{qt5dir}/mkspecs/hpuxi-*
%{qt5dir}/mkspecs/hurd-*
%{qt5dir}/mkspecs/irix-*
%{qt5dir}/mkspecs/linux-*
%{qt5dir}/mkspecs/lynxos-*
%{qt5dir}/mkspecs/macx-*
%{qt5dir}/mkspecs/netbsd-*
%{qt5dir}/mkspecs/openbsd-*
%{qt5dir}/mkspecs/qnx-*
%{qt5dir}/mkspecs/sco-*
%{qt5dir}/mkspecs/solaris-*
%{qt5dir}/mkspecs/tru64-*
%{qt5dir}/mkspecs/unixware-*
%{qt5dir}/mkspecs/unsupported
%{qt5dir}/mkspecs/win32-*
%{qt5dir}/mkspecs/wince60standard-*
%{qt5dir}/mkspecs/wince70embedded-*
%{qt5dir}/mkspecs/wince80colibri-*
%{qt5dir}/mkspecs/winphone-*
%{qt5dir}/mkspecs/winrt-*
%{qt5dir}/mkspecs/*.pri
