# TODO:
#	SBC plugin is missing bluez_sbc subdir
#	fix static libname (libopal_s.a)
#	IPv6 support requires IPv6 support in ptlib
#       SpanDSP FAX support requires t38_indicator symbol
#	MPEG4 rate control correction requires libavcodec sources
#       CAPI support
#	VPB support (--enable-libvpb, needs exceptions enabled in ptlib, BR: libvpb)
#
# WARNING: opal version should match Ekiga and ptlib versions
#      Recommendations: http://wiki.ekiga.org/index.php/Download_Ekiga_sources
#
# Conditional build:
%bcond_with	sip_fax_only	# Minimal build for t38modem + SIP
%bcond_without	celt		# CELT codec support
%bcond_with	srtp		# SRTP protocol support (mutually exclusive with zrtp)
%bcond_with	zrtp		# ZRTP protocol support [TODO: libzrtp[3]]
%bcond_with	capi		# CAPI [TODO: libcapi20, capi20.h]
%bcond_with	java		# Java JNI support
%bcond_with	ruby		# Ruby support
#
Summary:	Open Phone Abstraction Library (aka OpenH323 v2)
Summary(pl.UTF-8):	Biblioteka Open Phone Abstraction Library (aka OpenH323 v2)
Name:		opal
Version:	3.10.9
Release:	1
License:	MPL v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/opalvoip/%{name}-%{version}.tar.bz2
# Source0-md5:	f5dee986b7ae0d840bcc502785ea5bd7
Patch0:		%{name}-build.patch
Patch1:		%{name}-ffmpeg10.patch
Patch2:		%{name}-sh.patch
Patch3:		%{name}-libilbc.patch
Patch4:		%{name}-ah.patch
URL:		http://www.opalvoip.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_celt:BuildRequires:	celt-devel}
BuildRequires:	expat-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	ptlib-devel >= 1:2.10.9
BuildRequires:	sed >= 4.0
%if %{without sip_fax_only}
BuildRequires:	SDL-devel
# libavcodec >= 51.11.0 libavutil
BuildRequires:	ffmpeg-devel
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libgsm-devel
BuildRequires:	libtheora-devel
# ABI 0.102
BuildRequires:	libx264-devel >= 0.1.3-1.20101031_2245.1
BuildRequires:	webrtc-libilbc-devel
BuildRequires:	openssl-devel
%{?with_ruby:BuildRequires:	ruby-devel}
# with speexdsp
BuildRequires:	speex-devel >= 1:1.2
BuildRequires:	spandsp-devel
BuildRequires:	swig
BuildRequires:	unixODBC-devel
%endif
%requires_eq	ptlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	ptlib-devel >= 1:2.10.9

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPALDIR=`pwd`; export OPALDIR
OPAL_BUILD="yes"; export OPAL_BUILD
%{__aclocal}
%{__autoconf}
# don't run autoheader here, include/opal/buildopts.h.in is manually written
cd plugins
%{__aclocal}
%{__autoconf}
%{__autoheader}
cd ..
# Run  grep '^OPAL_.*=' configure.ac|grep 'yes\|no'  to check current defaults
%configure \
%if %{with sip_fax_only}
	--disable-aec \
	--disable-g711plc \
	--disable-h224 \
	--disable-h281 \
	--disable-h323 \
	--disable-h450 \
	--disable-h460 \
	--disable-h501 \
	--disable-iax \
	--disable-ivr \
	--disable-java \
	--disable-lid \
	--disable-plugins
	--disable-rfc4103 \
	--disable-rfc4175 \
	--disable-sipim \
	--disable-video \
%else
	%{?with_capi:--enable-capi} \
	%{!?with_celt:--disable-celt} \
	--enable-ixj \
	%{?with_java:--enable-java} \
	%{?with_ruby:--enable-ruby} \
	%{?with_srtp:--enable-srtp} \
	%{?with_zrtp:--enable-zrtp}
%endif

%{__make} %{?debug:debug}%{!?debug:opt} \
	CC="%{__cc}" \
	CPLUS="%{__cxx}" \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}" \
	VERBOSE=1

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
%{__sed} \
	-e 's,^OPALDIR.*=.*$,OPALDIR\t\t\t\t= %{_libdir}/opal-%{version},;' \
	-e 's,^OPAL_SRCDIR.*=.*$,OPAL_SRCDIR\t\t\t= %{_usrsrc}/debug/opal-%{version},;' \
	-e 's,^OPAL_INCDIR.*=.*$,OPAL_INCDIR\t\t\t= %{_includedir}/opal,;' \
	-e 's,^OPAL_LIBDIR.*=.*$,OPAL_LIBDIR\t\t\t= %{_libdir},;' \
	opal_defs.mak > $RPM_BUILD_ROOT%{_includedir}/opal/opal_defs.mak
cp -p opal_inc.mak $RPM_BUILD_ROOT%{_includedir}/opal

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopal.so.%{version}
%if %{without sip_fax_only}
%attr(755,root,root) %{_bindir}/simpleopal
%dir %{_libdir}/opal-%{version}
%dir %{_libdir}/opal-%{version}/codecs
%dir %{_libdir}/opal-%{version}/codecs/audio
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
%dir %{_libdir}/opal-%{version}/codecs/video
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h261_vic_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h263_ffmpeg_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h264_video_pwplugin_helper
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h264_x264_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/mpeg4_ffmpeg_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/theora_ptplugin.so
%dir %{_libdir}/opal-%{version}/fax
%attr(755,root,root) %{_libdir}/opal-%{version}/fax/spandsp_ptplugin.so
%dir %{_libdir}/opal-%{version}/lid
%attr(755,root,root) %{_libdir}/opal-%{version}/lid/ixj_lid_pwplugin.so
#%attr(755,root,root) %{_libdir}/opal-%{version}/lid/vpb_lid_pwplugin.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopal.so
%{_includedir}/opal
%{_pkgconfigdir}/opal.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopal_s.a
