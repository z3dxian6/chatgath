## **Modbus Scanner dans Metasploit**

### **Introduction**

Ce projet décrit comment créer et intégrer un module personnalisé dans Metasploit pour scanner des services **Modbus** sans dépendre d'un **UNIT_ID** précis. L'objectif est de détecter les services Modbus actifs en testant toutes les adresses **UNIT_ID** disponibles (1 à 255).

### **Structure du répertoire**

Voici la structure des fichiers nécessaires :

```
~/.msf4/
└── modules/
    └── auxiliary/
        └── scanner/
            └── scada/
                └── modbus_scanner.rb
```

### **Prérequis**

- **Kali Linux** (ou un autre environnement avec Metasploit installé)
- Accès au répertoire `~/.msf4/modules/`
- Connaissance des bases de Modbus et Ruby pour personnaliser le code.

### **Étapes d'intégration**

#### **1. Créer le répertoire pour les modules personnalisés**

Exécutez cette commande pour créer l'arborescence des répertoires où sera stocké le module :

```bash
mkdir -p ~/.msf4/modules/auxiliary/scanner/scada
```

#### **2. Ajouter le code du module**

Créez le fichier Ruby pour le module personnalisé :

```bash
nano ~/.msf4/modules/auxiliary/scanner/scada/modbus_scanner.rb
```

Collez ensuite le code suivant dans le fichier **modbus_scanner.rb** :

```ruby
class MetasploitModule < Msf::Auxiliary
  include Msf::Exploit::Remote::Tcp
  include Msf::Auxiliary::Scanner

  def initialize
    super(
      'Name'        => 'Modbus Service Scanner Without UNIT_ID',
      'Description' => %q{
        This module detects the Modbus service by scanning all potential UNIT_IDs (1 to 255).
        It sends a generic Modbus request and identifies which UNIT_IDs respond.
      },
      'References'  =>
        [
          [ 'URL', 'https://en.wikipedia.org/wiki/Modbus' ]
        ],
      'Author'      => [ 'Adapted from EsMnemon <esm[at]mnemonic.no>' ],
      'DisclosureDate' => 'Sep 5 2023',
      'License'     => MSF_LICENSE
    )

    register_options(
      [
        Opt::RPORT(502),
        OptInt.new('TIMEOUT', [true, 'Timeout for the network probe', 10])
      ])
  end

  def run_host(ip)
    # Loop over all possible UNIT_IDs (1..255)
    (1..255).each do |unit_id|
      vprint_status("#{ip}:#{rport} - Scanning Modbus UNIT_ID #{unit_id}")

      # Send a generic Modbus request (Function code 0x04: Read Input Registers)
      sploit = "\x21\x00\x00\x00\x00\x06\x01\x04\x00\x01\x00\x00"
      sploit[6] = [unit_id].pack("C")

      begin
        connect()
        sock.put(sploit)
        data = sock.get_once(nil, datastore['TIMEOUT'])

        if data && data[0, 4] == "\x21\x00\x00\x00"
          print_good("#{ip}:#{rport} - MODBUS - Detected service (UNIT_ID: #{unit_id})")
        else
          vprint_error("#{ip}:#{rport} - MODBUS - No response for UNIT_ID #{unit_id}")
        end

      rescue ::Rex::ConnectionError
        print_error("#{ip}:#{rport} - Connection failed.")
        return
      ensure
        disconnect()
      end
    end
  end
end
```

#### **3. Vérifier les permissions**

Assurez-vous que le fichier possède les permissions correctes pour être utilisé par Metasploit :

```bash
chmod 644 ~/.msf4/modules/auxiliary/scanner/scada/modbus_scanner.rb
```

#### **4. Charger le module dans Metasploit**

Lancez Metasploit :

```bash
msfconsole
```

Puis, chargez le module personnalisé :

```bash
use auxiliary/scanner/scada/modbus_scanner
```

#### **5. Configurer et exécuter le module**

1. Configurez les options nécessaires, par exemple :

```bash
set RHOSTS <adresse_IP_cible>
set TIMEOUT 10
```

2. Lancez le scan :

```bash
run
```

### **Résolution des problèmes**

1. **Module non détecté ?**
   - Vérifiez le chemin du fichier :
     ```bash
     ~/.msf4/modules/auxiliary/scanner/scada/modbus_scanner.rb
     ```
   - Redémarrez Metasploit après avoir ajouté le fichier.

2. **Erreur de syntaxe ?**
   - Vérifiez la syntaxe du fichier Ruby.

3. **Pas de réponse Modbus ?**
   - Assurez-vous que la cible écoute bien sur le port 502.
   - Testez la connectivité réseau avec un outil comme `nmap`.

---

### **Améliorations possibles**

- Ajouter des fonctionnalités pour lire/écrire dans les registres Modbus.
- Implémenter un mode "verbose" pour afficher les trames complètes.

### **Licence**

Ce projet est soumis à la licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.

---

Avec ce README, l'intégration de votre module personnalisé dans Metasploit devient simple et professionnelle !
