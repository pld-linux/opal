# TODO:
#	fix static libname (libopal_s.a)
#	IPv6 support requires IPv6 support in ptlib
#	x264+ffmpeg detection sucks - it doesn't work with --as-needed
#       SpanDSP FAX support requires t38_indicator symbol
#	MPEG4 rate control correction requires libavcodec sources
#       CAPI support
#
# WARNING: opal version should match Ekiga and ptlib versions
#      Recommendations: http://wiki.ekiga.org/index.php/Download_Ekiga_sources
#
# Conditional build:
%bcond_with	sip_fax_only	# Minimal build for t38modem + SIP
%bcond_without	celt		# Build with CELT codec support
#
# Don't touch this! strip removes all symbols from library
%define		no_install_post_strip		1
#
Summary:	Open Phone Abstraction Library (aka OpenH323 v2)
Summary(pl.UTF-8):	Biblioteka Open Phone Abstraction Library (aka OpenH323 v2)
Name:		opal
Version:	3.10.8
Release:	0.1
License:	MPL
Group:		Libraries
URL:		http://www.opalvoip.org
Source0:	http://downloads.sourceforge.net/opalvoip/%{name}-%{version}.tar.bz2
# Source0-md5:	b4907073e00889a9e7c6c49d41e4e2d4
Patch0:		%{name}-libname.patch
Patch1:		%{name}-mak_files.patch
Patch2:		%{name}-ac.patch
Patch3:		%{name}-build.patch
Patch4:		opal-3.10.8-svn-revision.patch
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_celt:BuildRequires:	celt-devel}
BuildRequires:	expat-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	ptlib-devel >= 1:2.10.8
BuildRequires:	sed >= 4.0
%{?with_celt:Requires:	celt}
%if %{without sip_fax_only}
BuildRequires:	SDL-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	libgsm-devel
BuildRequires:	libtheora-devel
BuildRequires:	libx264-devel
BuildRequires:	openssl-devel
BuildRequires:	speex-devel >= 1:1.1.5
BuildRequires:	unixODBC-devel
%endif
%requires_eq	ptlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_ld    -Wl,--as-needed

%description
The OPAL project aims to create a full featured, interoperable, Open
Source implementation of the ITU H.323 teleconferencing protocol that
can be used by personal developers and commercial users without
charge.

%description -l pl.UTF-8
Celem projektu OPAL jest stworzenie w pełni funkcjonalnej i
wyposażonej implementacji protokołu telekonferencyjnego ITU H.323,
który może być używany przez użytkowników prywatnych i komercyjnych
bez opłat.

%package devel
Summary:	Opal development files
Summary(pl.UTF-8):	Pliki dla developerów Opal
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	ptlib-devel

%description devel
Header files and libraries for developing applications that use OPAL.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki konieczne do rozwoju aplikacji
używających OPAL.

%package static
Summary:	OPAL static libraries
Summary(pl.UTF-8):	Biblioteki statyczne OPAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
OPAL static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OPAL.

%prep
%setup -q
#patch0 -p1
#patch1 -p1
#patch2 -p1
%patch3 -p1
%patch4 -p1

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPALDIR=`pwd`; export OPALDIR
OPAL_BUILD="yes"; export OPAL_BUILD
%{__aclocal}
%{__autoconf}
cd plugins
%{__aclocal}
%{__autoconf}
cd ..
# Run  grep '^OPAL_.*=' configure.ac|grep 'yes\|no'  to check current defaults
%configure \
%if %{with sip_fax_only}
	--enable-sip \
	--enable-t38 \
	--enable-fax \
	--enable-statistics \
	--disable-java \
	--disable-video \
	--disable-h323 \
	--disable-iax \
	--disable-h224 \
	--disable-h281 \
	--disable-sipim \
	--disable-rfc4103 \
	--disable-h450 \
	--disable-h460 \
	--disable-h501 \
	--disable-lid \
	--disable-ivr \
	--disable-rfc4175 \
	--disable-aec \
	--disable-g711plc \
	--disable-plugins
%else
%{!?with_celt:--disable-celt} \
	--enable-ixj
%endif

%{__make} %{?debug:debug}%{!?debug:opt} \
	CC="%{__cc}" \
	CPLUS="%{__cxx}" \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}"

%{__cp} -a */libopal* .
%if %{without sip_fax_only}
%{__make} -C samples/simple %{?debug:debug}%{!?debug:opt} \
	CC="%{__cc}" \
	CPLUS="%{__cxx}" \
	CFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG} -I`pwd`/include" \
	LDFLAGS="%{rpmldflags} -L`pwd` -lpt -lopal"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

%{!?with_sip_fax_only:install samples/simple/obj/simpleopal $RPM_BUILD_ROOT%{_bindir}}

# This needs to be done after 'make install'
sed -i -e \
's,^OPALDIR.*=.*$,OPALDIR\t\t\t\t= %{_libdir}/opal-%{version},;'\
's,^OPAL_SRCDIR.*=.*$,OPAL_SRCDIR\t\t\t= %{_usrsrc}/debug/opal-%{version},;'\
's,^OPAL_INCDIR.*=.*$,OPAL_INCDIR\t\t\t= %{_includedir}/opal,;'\
's,^OPAL_LIBDIR.*=.*$,OPAL_LIBDIR\t\t\t= %{_libdir},;' \
opal_defs.mak

install opal_{inc,defs}.mak $RPM_BUILD_ROOT%{_includedir}/opal

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%if %{without sip_fax_only}
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/opal-%{version}
%dir %{_libdir}/opal-%{version}/codecs
%dir %{_libdir}/opal-%{version}/codecs/audio
%dir %{_libdir}/opal-%{version}/codecs/video
%dir %{_libdir}/opal-%{version}/lid
%{?with_celt:%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/celt_ptplugin.so}
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g722_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g7221_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g7222_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g726_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/gsm0610_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/gsmamrcodec_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/iLBC_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/ima_adpcm_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/lpc10_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/silk_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/speex_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h261_vic_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h263_ffmpeg_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h264_video_pwplugin_helper
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h264_x264_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/mpeg4_ffmpeg_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/theora_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/lid/ixj_lid_pwplugin.so
#%attr(755,root,root) %{_libdir}/opal-%{version}/lid/vpb_lid_pwplugin.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/opal
%{_pkgconfigdir}/opal.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
