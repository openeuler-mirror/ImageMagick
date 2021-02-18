Name:           ImageMagick
Epoch:          1
Version:        6.9.10.67
Release:        10
Summary:        Create, edit, compose, or convert bitmap images
License:        ImageMagick and MIT
Url:            http://www.imagemagick.org/
Source0:        https://mirrors.sohu.com/gentoo/distfiles/db/ImageMagick-6.9.10-67.tar.xz

Patch0001:      CVE-2019-7397.patch
Patch0002:      CVE-2018-16329.patch
Patch0003:      CVE-2020-27759.patch
Patch0004:      CVE-2020-27760.patch
Patch0005:      CVE-2020-27761.patch
Patch0006:      CVE-2020-27762.patch
Patch0007:      CVE-2020-27764.patch
Patch0008:      CVE-2020-27765.patch
Patch0009:      CVE-2020-27766.patch
Patch0010:      CVE-2020-27767.patch
Patch0011:      CVE-2020-27770.patch
Patch0012:      CVE-2020-29599-1.patch
Patch0013:      CVE-2020-29599-2.patch
Patch0014:      CVE-2020-29599-3.patch
Patch0015:      CVE-2020-29599-4.patch
Patch0016:      CVE-2020-29599-5.patch
Patch0017:      CVE-2020-29599-6.patch
Patch0018:      CVE-2020-29599-7.patch
Patch0019:      CVE-2020-29599-8.patch
Patch0020:      CVE-2020-29599-9.patch
Patch0021:      CVE-2020-29599-10.patch
Patch0022:      CVE-2020-27754-pre-1.patch
Patch0023:      CVE-2020-27754-pre-2.patch
Patch0024:      CVE-2020-27754.patch
Patch0025:      CVE-2020-25664.patch

BuildRequires:  bzip2-devel freetype-devel libjpeg-devel libpng-devel perl-generators
BuildRequires:  libtiff-devel giflib-devel zlib-devel perl-devel >= 5.8.1 jbigkit-devel
BuildRequires:  libgs-devel ghostscript-x11 libwmf-devel 
BuildRequires:  libtool-ltdl-devel libX11-devel libXext-devel libXt-devel lcms2-devel
BuildRequires:  libxml2-devel librsvg2-devel fftw-devel ilmbase-devel OpenEXR-devel
BuildRequires:  openjpeg2-devel >= 2.1.0 libwebp-devel autoconf automake gcc gcc-c++

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
%autosetup -n ImageMagick-6.9.10-67 -p1

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
cp -a www/source %{buildroot}%{_datadir}/doc/ImageMagick-6.9.10
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
%{_libdir}/libMagickCore-6.Q16.so.6*
%{_libdir}/libMagickWand-6.Q16.so.6*
%{_libdir}/ImageMagick-6.9.10
%{_datadir}/ImageMagick-6
%dir %{_sysconfdir}/ImageMagick-6
%config(noreplace) %{_sysconfdir}/ImageMagick-6/*.xml

%files devel
%{_bindir}/MagickCore-config
%{_bindir}/Magick-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/libMagickCore-6.Q16.so
%{_libdir}/libMagickWand-6.Q16.so
%{_libdir}/pkgconfig/MagickCore*
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-6.Q16.pc
%{_libdir}/pkgconfig/MagickWand*
%{_libdir}/pkgconfig/Wand*
%dir %{_includedir}/ImageMagick-6
%{_includedir}/%{name}-6/magick
%{_includedir}/%{name}-6/wand

%files help
%doc README.txt NEWS.txt ChangeLog Platforms.txt QuickStart.txt
%doc %{_datadir}/doc/ImageMagick-6
%doc %{_datadir}/doc/ImageMagick-6.9.10
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files perl -f perl-pkg-files
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt

%files c++
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++-6.Q16.so.8*

%files c++-devel
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/ImageMagick-6/Magick++*
%{_libdir}/libMagick++-6.Q16.so
%{_libdir}/pkgconfig/Magick++*
%{_libdir}/pkgconfig/ImageMagick++*

%changelog
* Wed Feb 10 2021 zhanghua <zhanghua40@huawei.com> - 6.9.10.67-10
- fix CVE-2020-25664 CVE-2020-27754

* Wed Jan 13 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-9
- fix CVE-2020-29599

* Mon Jan 04 2021 wangxiao <wangxiao65@huawei.com> - 6.9.10.67-8
- fix CVE-2018-16329 CVE-2020-27759 CVE-2020-27760 CVE-2020-27761 CVE-2020-27762
  CVE-2020-27764 CVE-2020-27765 CVE-2020-27765 CVE-2020-27766 CVE-2020-27767 CVE-2020-27770

* Tue May 19 2020 fengtao <fengtao40@huawei.com> - 6.9.10.67-7
- rebuild for libwebp-1.1.0

* Tue Mar 10 2020 songnannan <songnannan2@huawei.com> - 6.9.10.67-6
- delete the jasper

* Mon Feb 24 2020 xuxijian<xuxijian@huawei.com> - 6.9.10.67-5 
- Package init
