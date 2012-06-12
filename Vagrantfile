# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  # Builder
  config.vm.define :builder do |t|
    t.vm.box = "centos58-builder"
  end

  # Test
  config.vm.define :test do |t|
    t.vm.box = "centos58"
    t.vm.forward_port 80, 8002
  end
end
