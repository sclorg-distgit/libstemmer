%{?scl:%scl_package libstemmer}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}libstemmer
Version:	0
Release:	5.585svn%{?dist}
Summary:	C stemming algorithm library
# The site and project is no longer being actively maintained. 
# The code is available on Github - https://github.com/snowballstem/snowball
URL:		http://snowball.tartarus.org
# The licence is specified on website
# http://snowball.tartarus.org/license.php
# There is a pull request to include it into source code
# https://github.com/snowballstem/snowball/issues/10
License:	BSD
Source0:	http://snowball.tartarus.org/dist/%{pkg_name}_c-svn585.tgz
Source1:	Notice.txt
Source2:	BSD.txt

%{?scl:Requires:%scl_runtime}

%description
Snowball stemming algorithms for use in Information Retrieval Snowball 
provides access to efficient algorithms for calculating a "stemmed" 
form of a word.  This is a form with most of the common morphological 
endings removed; hopefully representing a common linguistic base form.  
This is most useful in building search engines and information 
retrieval software; for example, a search with stemming enabled should 
be able to find a document containing "cycling" given the query 
"cycles".

Snowball provides algorithms for several (mainly European) languages. 
It also provides access to the classic Porter stemming algorithm for 
English: although this has been superseded by an improved algorithm, 
the original algorithm may be of interest to information retrieval 
researchers wishing to reproduce results of earlier experiments.

%package devel
Summary:	C stemming algorithm library developer files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files of libstemmer.

Snowball stemming algorithms for use in Information Retrieval Snowball 
provides access to efficient algorithms for calculating a "stemmed" 
form of a word.  This is a form with most of the common morphological 
endings removed; hopefully representing a common linguistic base form.  
This is most useful in building search engines and information 
retrieval software; for example, a search with stemming enabled should 
be able to find a document containing "cycling" given the query 
"cycles".

Snowball provides algorithms for several (mainly European) languages. 
It also provides access to the classic Porter stemming algorithm for 
English: although this has been superseded by an improved algorithm, 
the original algorithm may be of interest to information retrieval 
researchers wishing to reproduce results of earlier experiments.

%prep
%setup -q -n libstemmer_c

# Add rule to make libstemmer.so
sed -i -r "s|(^libstemmer.o:)|libstemmer.so: \$\(snowball_sources:.c=.o\)\n\
\t\$\(CC\) \$\(CFLAGS\) -shared \$\(LDFLAGS\) -Wl,-soname,libstemmer.so.%{?scl_prefix}0 \
-o \$\@.%{?scl_prefix}0.0.0 \$\^\n\1|" Makefile

%build
make libstemmer.so %{?_smp_mflags} CFLAGS="%{optflags} -fPIC -Iinclude"

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install -p -D -m 755	libstemmer.so.%{?scl_prefix}0.0.0	%{buildroot}%{_libdir}/
ln -s libstemmer.so.%{?scl_prefix}0.0.0	%{buildroot}%{_libdir}/libstemmer.so.%{?scl_prefix}0
ln -s libstemmer.so.%{?scl_prefix}0.0.0	%{buildroot}%{_libdir}/libstemmer.so
install -p -D -m 644	include/*	%{buildroot}%{_includedir}/

cp %{SOURCE1} %{SOURCE2} .

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc Notice.txt BSD.txt README
%{_libdir}/libstemmer.so.*

%files devel
%{_libdir}/libstemmer.so
%{_includedir}/*

%changelog
* Wed Mar 18 2015 Marek Skalicky <mskalick@redhat.com> - 0-5.585svn
- Rebuilt for 'scls' removal

* Mon Jan 26 2015 Marek Skalicky <mskalick@redhat.com> - 0-4.585svn
- Added scl_runtime requires

* Sun Jan 18 2015 Honza Horak <hhorak@redhat.com> - 0-3.585svn
- Convert to scl package

* Tue Jan 6 2015 Marek Skalicky <mskalick@redhat.com> - 0-2.585svn
- Removed undefined-non-weak-symbol warnings

* Tue Dec 2 2014 Marek Skalicky <mskalick@redhat.com> - 0-1.585svn
- Initial packaging
