# TODO:
#	SBC plugin is missing bluez_sbc subdir
#	fix static libname (libopal_s.a)
#	MPEG4 rate control correction requires libavcodec sources
# NOTE: IPv6 support requires IPv6 support in ptlib
#
# WARNING: opal version should match Ekiga and ptlib versions
#	Recommendations: http://wiki.ekiga.org/index.php/Download_Ekiga_sources
#	(for ekiga 4.0.x it's ptlib 2.10.x + opal 3.10.x)
#
# Conditional build:
%bcond_with	sip_fax_only	# minimal build for t38modem + SIP
%bcond_without	celt		# CELT codec support
%bcond_without	srtp		# SRTP protocol support (mutually exclusive with zrtp)
%bcond_with	zrtp		# ZRTP protocol support (mutually exclusive with srtp; broken as of 3.10.9)
%bcond_without	capi		# CAPI support
%bcond_without	vpb		# Voicetronix VPB support
%bcond_with	java		# Java JNI interface (only swig wrapper, Java part not built)
%bcond_with	ruby		# Ruby interface (very initial, only swig wrapper)
#
%if %{with zrtp}
%undefine	with_srtp
%endif
%if %{with sip_fax_only}
%undefine	with_java
%undefine	with_ruby
%undefine	with_srtp
%undefine	with_zrtp
%endif
Summary:	Open Phone Abstraction Library (aka OpenH323 v2)
Summary(pl.UTF-8):	Biblioteka Open Phone Abstraction Library (aka OpenH323 v2)
Name:		opal
Version:	3.10.11
Release:	4
License:	MPL v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/opalvoip/%{name}-%{version}.tar.bz2
# Source0-md5:	fc36a30d2cbce0fbf7cb6ef33b8d63c3
Patch0:		%{name}-build.patch
Patch1:		ffmpeg.patch
Patch2:		%{name}-sh.patch
Patch3:		%{name}-libilbc.patch
Patch4:		%{name}-ah.patch
Patch5:		%{name}-exceptions.patch
Patch6:		%{name}-ruby.patch
Patch7:		srtp.patch
URL:		http://www.opalvoip.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_capi:BuildRequires:	capi4k-utils-devel}
%{?with_celt:BuildRequires:	celt-devel}
BuildRequires:	expat-devel
BuildRequires:	libstdc++-devel
%{?with_zrtp:BuildRequires:	libzrtp-devel}
BuildRequires:	pkgconfig
BuildRequires:	ptlib-devel >= 1:2.10.9
BuildRequires:	sed >= 4.0
BuildRequires:	speex-devel >= 1:1.2
BuildRequires:	speexdsp-devel >= 1.2
%{?with_srtp:BuildRequires:	libsrtp2-devel}
%if %{without sip_fax_only}
BuildRequires:	SDL-devel
# libavcodec >= 51.11.0 libavutil
BuildRequires:	ffmpeg-devel
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libgsm-devel
BuildRequires:	libtheora-devel
%{?with_vpb:BuildRequires:	vpb-devel}
# ABI 0.102
BuildRequires:	libx264-devel >= 0.1.3-1.20101031_2245.1
BuildRequires:	webrtc-libilbc-devel
BuildRequires:	openssl-devel
%{?with_ruby:BuildRequires:	ruby-devel}
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

%package lid-vpb
Summary:	Opal LID plugin for Voicetronix VPB devices
Summary(pl.UTF-8):	Wtyczka Opal LID dla urządzeń VPB firmy Voicetronix
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description lid-vpb
Opal LID plugin for Voicetronix VPB devices.

%description lid-vpb -l pl.UTF-8
Wtyczka Opal LID dla urządzeń VPB firmy Voicetronix.

%package devel
Summary:	Opal development files
Summary(pl.UTF-8):	Pliki dla developerów Opal
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_capi:Requires:	capi4k-utils-devel}
Requires:	libstdc++-devel
%{?with_zrtp:Requires:	libzrtp-devel}
Requires:	ptlib-devel >= 1:2.10.9
Requires:	speex-devel >= 1:1.2
%{?with_srtp:Requires:	libsrtp2-devel}

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
%patch5 -p1
%patch6 -p1
%patch7 -p1

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
	CFLAGS="%{rpmcflags} -std=gnu++98" \
	CXXFLAGS="%{rpmcxxflags} -std=gnu++98" \
	%{?with_java:JDK_ROOT=%{_jvmdir}/java} \
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
	--disable-lid \
	--disable-plugins
	--disable-rfc4103 \
	--disable-rfc4175 \
	--disable-sipim \
	--disable-video \
%else
	--enable-ixj \
%endif
	%{!?with_capi:--disable-capi} \
	%{!?with_celt:--disable-celt} \
	%{!?with_java:--disable-java} \
	%{!?with_ruby:--disable-ruby} \
	%{!?with_srtp:--disable-srtp} \
	%{?with_vpb:--enable-vpb} \
%if %{with zrtp}
	--enable-zrtp \
	--with-bn-includedir=/usr/include \
	--with-bn-libdir=%{_libdir} \
	--with-zrtp-includedir=/usr/include/libzrtp \
	--with-zrtp-libdir=%{_libdir}
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
%endif

%if %{with vpb}
%files lid-vpb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opal-%{version}/lid/vpb_ptplugin.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopal.so
%{_includedir}/opal
%{_pkgconfigdir}/opal.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopal_s.a
