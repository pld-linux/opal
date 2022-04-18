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
%bcond_with	capi		# CAPI support
%bcond_with	vpb		# Voicetronix VPB support
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
Version:	3.18.8
Release:	1
License:	MPL v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/opalvoip/%{name}-%{version}.tar.bz2
# Source0-md5:	1f48ea0bef4b0731b4af19928eb02c36
Patch0:		celt.patch
Patch1:		g7221.patch
Patch2:		%{name}-cxx11.patch
# domain suspended (2022.04)
#URL:		http://www.opalvoip.org/
URL:		https://sourceforge.net/projects/opalvoip/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_capi:BuildRequires:	capi4k-utils-devel}
%{?with_celt:BuildRequires:	celt-devel}
BuildRequires:	expat-devel
%{?with_srtp:BuildRequires:	libsrtp2-devel}
BuildRequires:	libstdc++-devel
%{?with_zrtp:BuildRequires:	libzrtp-devel}
BuildRequires:	pkgconfig
BuildRequires:	ptlib-devel >= 1:2.18.5
BuildRequires:	sed >= 4.0
BuildRequires:	speex-devel >= 1:1.2
BuildRequires:	speexdsp-devel >= 1.2
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
BuildRequires:	openh264-devel
BuildRequires:	openssl-devel
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	spandsp-devel
BuildRequires:	swig
BuildRequires:	unixODBC-devel
BuildRequires:	webrtc-libilbc-devel
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
%{?with_capi:Requires: capi4k-utils-devel}
%{?with_srtp:Requires: libsrtp2-devel}
Requires:	libstdc++-devel
%{?with_zrtp:Requires: libzrtp-devel}
Requires:	ptlib-devel >= 1:2.18.5
Requires:	speex-devel >= 1:1.2

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

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPALDIR=`pwd`; export OPALDIR
OPAL_BUILD="yes"; export OPAL_BUILD
cd plugins
%{__aclocal}
%{__autoconf}
cd ..
# Run  grep '^OPAL_.*=' configure.ac|grep 'yes\|no'  to check current defaults
%configure \
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
	--disable-dahdi \
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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/opal-%{version}/lid

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopal.so.%{version}
%if %{without sip_fax_only}
%dir %{_libdir}/opal-%{version}
%dir %{_libdir}/opal-%{version}/codecs
%dir %{_libdir}/opal-%{version}/codecs/audio
%{?with_celt:%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/celt_ptplugin.so}
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g7221_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g7222_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g722_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/g726_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/gsm0610_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/gsmamrcodec_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/iLBC_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/ima_adpcm_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/iSAC_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/lpc10_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/opus_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/silk_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/speex_ptplugin.so
%dir %{_libdir}/opal-%{version}/codecs/video
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h261_vic_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h263_ffmpeg_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h264_video_pwplugin_helper
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/h264_x264_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/mpeg4_ffmpeg_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/openh264_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/theora_ptplugin.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/vp8_webm_ptplugin.so
%dir %{_libdir}/opal-%{version}/fax
%attr(755,root,root) %{_libdir}/opal-%{version}/fax/spandsp_ptplugin.so
%endif
%dir %{_libdir}/opal-%{version}/lid

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
%{_datadir}/opal

%files static
%defattr(644,root,root,755)
%{_libdir}/libopal_s.a
