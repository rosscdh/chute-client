# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "debian/jessie64"

    config.vm.network "private_network", ip: "192.168.33.11"

    config.vm.provision "ansible" do |ansible|
        ansible.verbose = "vv"
        ansible.playbook = "/Users/rosscdh/p/chute/ansible-raspberry-pi/new-raspberry/setup.yml"
    end

    config.vm.provider "virtualbox" do |vb, override|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end
end

