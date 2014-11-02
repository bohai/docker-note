#Build ISO  
yum install -y git livecd-tools createrepo rpm-build  
ln -s /rpmbuild /root/rpmbuild  

#docker start  
touch /etc/resolve.conf  
docker -d -H unix:///run/docker.sock  
chkconfig docker on  

#etcd  
http://mirrors.aliyun.com/fedora/updates/20/SRPMS/etcd-0.4.6-6.fc20.src.rpm  


