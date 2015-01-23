# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    config.vm.provision "shell", path: "provision.sh"

    config.vm.provider "virtualbox" do |vb, override|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end

    config.vm.network "forwarded_port", guest: 5000, host: 5000
    config.vm.network "forwarded_port", guest: 80, host: 5080
    config.vm.synced_folder ".", "/var/apps/chute-client/versions/chute-client"
    config.vm.synced_folder "../conf", "/home/vagrant/conf"
end

