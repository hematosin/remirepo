%global gh_owner    couchbase
%global gh_commit   b2ad9312dfe25c792b03231166c80cf5761cafdd
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})

# Tests require some need which are downloaded during make
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}

Name:          libcouchbase
Version:       2.0.5
Release:       1%{?dist}
Summary:       Couchbase client library
Group:         System Environment/Libraries
License:       ASL 2.0
URL:           http://www.couchbase.com/develop/c/current
Source0:       https://github.com/%{gh_owner}/%{name}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf
BuildRequires: cyrus-sasl-devel


%description
The C library provides fast access to documents in Couchbase Server 2.0.
With JSON documents and Couchbase server 2.0 you have new ways to index
and query data stored in the cluster through views. This client library,
libcouchbase, also simplifies requests to Views through its handling of
HTTP transport.

This Couchbase Client Library for C and C++ provides a complete interface
to the functionality of Couchbase Server.


%package       devel
Summary:       Development files for Couchbase client library
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package       tools
Summary:       Couchbase tools
Group:         Applications/System
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package contains some command line tools to manage
a Couchbase Server.


%prep
%setup -qn %{name}-%{gh_commit}

cat <<EOF | tee m4/version.m4
m4_define([VERSION_NUMBER], [%{version}])
m4_define([GIT_CHANGESET],[%{gh_commit}])
EOF


%build
autoreconf -i --force
%{configure} \
%if ! %{with_tests}
    --disable-tests \
    --disable-couchbasemock \
%endif
    --enable-system-libsasl

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

# Remove uneeded files
rm -f %{buildroot}%{_libdir}/*.la


%files
%defattr(-,root,root,-)
%doc LICENSE RELEASE_NOTES.markdown
%{_libdir}/%{name}.so.*
# Plugins
%{_libdir}/%{name}_libevent.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_mandir}/man3/couch*
%{_mandir}/man3/lcb*
%{_mandir}/man5/lcb*
%{_libdir}/%{name}.so

%files tools
%defattr(-,root,root,-)
%{_bindir}/cbc*
%{_mandir}/man1/cbc*
%{_mandir}/man5/cbc*

%check
%if %{with_tests}
%else
: check disabled, missing '--with tests' option
%endif


%changelog
* Sun Apr 14 2013 Remi Collet <remi@feoraproject.org> - 2.0.5-1
- Initial package
