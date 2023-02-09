Name:           ImageMagick
Epoch:          1
Version:        7.1.0.28
Release:        5
Summary:        Create, edit, compose, or convert bitmap images
License:        ImageMagick and MIT
Url:            http://www.imagemagick.org/
Source0:        https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.0-28.tar.gz

Patch0001: backport-fix-CVE-2022-2719.patch
Patch0002: backport-fix-CVE-2022-1115.patch
Patch0003: CVE-2022-32547.patch
Patch0004: CVE-2022-44267_CVE-2022-44268.patch
Patch0005: CVE-2022-3213-pre1.patch
Patch0006: CVE-2022-3213-pre2.patch
Patch0007: CVE-2022-3213-pre3.patch
Patch0008: CVE-2022-3213.patch

BuildRequires:  bzip2-devel freetype-devel libjpeg-devel libpng-devel perl-generators
BuildRequires:  libtiff-devel giflib-devel zlib-devel perl-devel >= 5.8.1 jbigkit-devel
BuildRequires:  libgs-devel ghostscript-x11 libwmf-devel 
BuildRequires:  libtool-ltdl-devel libX11-devel libXext-devel libXt-devel lcms2-devel
BuildRequires:  libxml2-devel librsvg2-devel fftw-devel Imath-devel OpenEXR-devel
BuildRequires:  openjpeg2-devel >= 2.1.0 libwebp-devel autoconf automake gcc gcc-c++ open-sans-fonts

Requires:       open-sans-fonts

Provides:       ImageMagick-libs = %{epoch}:%{version}-%{release}
Provides:       ImageMagick-djva = %{epoch}:%{version}-%{release}
Obsoletes:      ImageMagick-libs < %{epoch}:%{version}-%{release}
Obsoletes:      ImageMagick-djvu < %{epoch}:%{version}-%{release}

%description
Use ImageMagick to create, edit, compose, or convert bitmap images. It can read and write
images in a variety of formats (over 200) including PNG, JPEG, GIF, HEIC, TIFF, DPX, EXR,
WebP, Postscript, PDF, and SVG. Use ImageMagick to resize, flip, mirror, rotate, distort,
shear and transform images, adjust image colors, apply various special effects,
or draw text, lines, polygons, ellipses and Bézier curves.

%package devel
Summary:        Development files for ImageMagick
Requires:       ImageMagick = %{epoch}:%{version}-%{release}
Requires:       libgs-devel libX11-devel libXext-devel libXt-devel
Requires:       bzip2-devel freetype-devel libtiff-devel libjpeg-devel lcms2-devel
Requires:       libwebp-devel OpenEXR-devel pkgconfig

%description devel
Development files for ImageMagick.

%package help
Summary:        HTML documentation for ImageMagick
Provides:       ImageMagick-doc = %{epoch}:%{version}-%{release}
Obsoletes:      ImageMagick-doc < %{epoch}:%{version}-%{release}

%description help
HTML documentation for ImageMagick.

%package perl
Summary:        Perl bindings to ImageMagick
Requires:       ImageMagick = %{epoch}:%{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl bindings to ImageMagick.
Install it to use perl scripts that use ImageMagick.

%package c++
Summary:        Magick++ library
Requires:       ImageMagick = %{epoch}:%{version}-%{release}

%description c++
This package contains the Magick++ library.
Install it to use applications that use Magick++.

%package c++-devel
Summary:        Development files for ImageMagick-c++
Requires:       ImageMagick-c++ = %{epoch}:%{version}-%{release}
Requires:       ImageMagick-devel = %{epoch}:%{version}-%{release}

%description c++-devel
Development files for ImageMagick-c++.

%prep
%autosetup -n ImageMagick-7.1.0-28 -p1

install -d Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples

%build
autoconf -f -i
export CFLAGS="%{optflags} -DIMPNG_SETJMP_IS_THREAD_SAFE"
%configure --enable-shared --disable-static --with-modules --with-perl --with-x \
        --with-threads --with-magick_plus_plus --with-gslib --with-wmf --with-webp \
        --with-openexr --with-rsvg --with-xml --without-dps --without-gcc-arch \
        --with-jbig --with-openjp2 \
        --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'"
%make_build

%install
%make_install
cp -a www/source %{buildroot}%{_datadir}/doc/ImageMagick-7.1.0
rm %{buildroot}%{_libdir}/*.la

%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

find %{buildroot} -name "*.bs" -exec rm {} \;
find %{buildroot} -name ".packlist" -exec rm {} \;
find %{buildroot} -name "perllocal.pod" -exec rm {} \;

printf "%defattr(-,root,root,-)\n" > perl-pkg-files
find %{buildroot}/%{_libdir}/perl* -type f -print | sed "s@^%{buildroot}@@g" > perl-pkg-files
find %{buildroot}%{perl_vendorarch} -type d -print | sed "s@^%{buildroot}@%dir @g" \
        | grep -v '^%dir %{perl_vendorarch}$' | grep -v '/auto$' >> perl-pkg-files

%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}
make %{?_smp_mflags} check
rm PerlMagick/demo/Generic.ttf

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%doc LICENSE NOTICE AUTHORS.txt
%{_bindir}/[a-z]*
%{_libdir}/libMagickCore-7.Q16HDRI.so.10*
%{_libdir}/libMagickWand-7.Q16HDRI.so.10*
%{_libdir}/ImageMagick-7.1.0
%{_datadir}/ImageMagick-7
%dir %{_sysconfdir}/ImageMagick-7
%config(noreplace) %{_sysconfdir}/ImageMagick-7/*.xml

%files devel
%{_bindir}/MagickCore-config
%{_bindir}/MagickWand-config
%{_libdir}/libMagickCore-7.Q16HDRI.so
%{_libdir}/libMagickWand-7.Q16HDRI.so
%{_libdir}/pkgconfig/MagickCore*
%{_libdir}/pkgconfig/ImageMagick*.pc
%{_libdir}/pkgconfig/MagickWand*
%dir %{_includedir}/ImageMagick-7
%{_includedir}/%{name}-7/MagickWand/*
%{_includedir}/%{name}-7/MagickCore/*

%files help
%doc README.txt NEWS.txt ChangeLog.md QuickStart.txt
%doc %{_datadir}/doc/ImageMagick-7
%doc %{_datadir}/doc/ImageMagick-7.1.0
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files perl -f perl-pkg-files
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt

%files c++
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++-7.Q16HDRI.so.5*

%files c++-devel
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/ImageMagick-7/Magick++*
%{_libdir}/libMagick++-7.Q16HDRI.so
%{_libdir}/pkgconfig/Magick++*
%{_libdir}/pkgconfig/ImageMagick*

%changelog
* Thu Feb 09 2023 yaoxin <yaoxin30@h-partners.com> - 1:7.1.0.28-5
- Fix CVE-2022-44267,CVE-2022-44268 and CVE-2022-3213

* Tue Nov 22 2022 yaoxin <yaoxin30@h-partners.com> - 1:7.1.0.28-4
- Fix CVE-2022-32547

* Fri Aug 19 2022 cenhuilin <cenhuilin@kylinos.cn> - 1:7.1.0.28-3
- fix CVE-2022-1115

* Wed Aug 10 2022 cenhuilin <cenhuilin@kylinos.cn> - 1:7.1.0.28-2
- fix CVE-2022-2719

* Fri May 13 2022 houyingchao <houyingchao@h-partners.com> - 7.1.0.28-1
- Upgrade to 7.1.0.28 for fix CVE-2022-1114

* Thu Mar 10 2022 wangkai <wangkai385@huawei.com> - 7.1.0.27-1
- Update to 7.1.0.27 for fix CVE-2021-39212 CVE-2021-3596

* Thu Jun 03 2021 wangyue <wangyue92@huawei.com> - 6.9.10.67-25
- Fix CVE-2020-27756 CVE-2020-25667 CVE-2020-27753

* Tue May 25 2021 wangyue <wangyue92@huawei.com> - 6.9.10.67-24
- Fix CVE-2020-27769

* Thu May 20 2021 wangyue <wangyue92@huawei.com> - 6.9.10.67-23
- Fix CVE-2021-20309 CVE-2021-20311 CVE-2021-20312 CVE-2021-20313

* Thu Apr 29 2021 wangyue <wangyue92@huawei.com> - 6.9.10.67-22
- Fix CVE-2020-27752

* Mon Apr 12 2021 wangyue <wangyue92@huawei.com> - 6.9.10.67-21
- Fix CVE-2019-18853 CVE-2020-27755

* Tue Apr 6 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-20
- Fix CVE-2020-25666 CVE-2020-25675

* Wed Mar 31 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-19
- Fix CVE-2020-25676 CVE-2020-27757 CVE-2020-27758 CVE-2020-27771
  CVE-2020-27772 CVE-2020-27774 CVE-2020-27775 CVE-2020-27751

* Tue Mar 23 2021 zhanghua <zhanghua40@huawei.com> - 6.9.10.67-18
- Fix CVE-2021-20246

* Sat Mar 20 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-17
- Fix CVE-2021-20244

* Tue Mar 16 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-16
- Fix CVE-2021-20241 CVE-2021-20243

* Mon Mar 8 2021 zhanghua <zhanghua40@huawei.com> - 6.9.10.67-15
- Fix CVE-2020-27750 CVE-2020-25665 CVE-2020-25674

* Wed Mar 03 2021 wangyue <wangyue92@huawei.com> - 6.9.10.67-14
- Fix CVE-2020-27768

* Mon Mar 01 2021 wangyue <wangyue92@huawei.com> - 6.9.10.67-13
- Fix CVE-2020-27773 CVE-2020-27763

* Thu Feb 25 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-12
- Fix CVE-2021-20176

* Wed Feb 10 2021 zhanghua <zhanghua40@huawei.com> - 6.9.10.67-11
- fix CVE-2020-25664 CVE-2020-27754

* Wed Jan 13 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-10
- add MIT license

* Tue Jan 12 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-9
- fix CVE-2020-29599

* Mon Jan 04 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-8
- fix CVE-2020-27759 CVE-2020-27760 CVE-2020-27761 CVE-2020-27762 CVE-2020-27764
  CVE-2020-27765 CVE-2020-27765 CVE-2020-27766 CVE-2020-27767 CVE-2020-27770

* Sun Apr 26 2020 openEuler Buildteam <buildteam@openeuler.org> - 6.9.10.67-7
- Type:cves
- ID:CVE-2018-16329
- SUG:restart
- DESC:fix CVE-2018-16329

* Tue Mar 10 2020 songnannan <songnannan2@huawei.com> - 6.9.10.67-6
- delete the jasper

* Mon Feb 24 2020 xuxijian<xuxijian@huawei.com> - 6.9.10.67-5 
- Package init
