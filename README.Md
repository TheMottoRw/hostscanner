# Host scanner
#### To enable windows discovery on windows pc with enabled firewall
<code>Go to 
1. Control panel
2. System security
3. Windows firewall
4. Allow an app or feature
5. Tick in File and Printer sharing
</code>

### Installation and Tools required to run this application

1. Install python3,pip,virtualenv,mysql
2. nmap and ipscan
   <code>
3. References: 
      1. https://nmap.org/download
      2. https://github.com/angryip/ipscan/
      </code>
4. When installation of those tools done,go parent directory run <code>pip install -r requirements.txt</code>
5. Run application by
 <code>
   1. python app.py
   2. python controllers/Scanner.py
</code>