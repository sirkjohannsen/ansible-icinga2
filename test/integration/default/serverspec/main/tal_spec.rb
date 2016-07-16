require 'spec_helper'


describe package('icinga2') do
  it { should be_installed }
end

if os[:release] == "16.04"
  describe file("/etc/apt/sources.list.d/packages_icinga_org_ubuntu.list")  do
    its(:content) {should match "deb http://packages.icinga.org/ubuntu icinga-xenial main"}
  end
end

if os[:release] == "14.04"
  describe file("/etc/apt/sources.list.d/packages_icinga_org_ubuntu.list")  do
    its(:content) {should match "deb http://packages.icinga.org/ubuntu icinga-trusty main"}
  end
end
