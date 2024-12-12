# Chatgath

Pour modifier et ajouter un module personnalisé dans Metasploit sur votre Kali Linux, vous devez suivre ces étapes :

-> Localiser le répertoire des modules Metasploit
Les modules personnalisés doivent être placés dans le répertoire ~/.msf4/modules/ pour être reconnus par Metasploit. Si ce répertoire n'existe pas, vous devrez le créer.

Créez le répertoire pour les modules auxiliaires si ce n'est pas déjà fait :
mkdir -p ~/.msf4/modules/auxiliary/scanner/scada
Ce répertoire est où Metasploit recherche les modules ajoutés par l'utilisateur.

-> Créer un fichier pour le nouveau module
Créer un nouveau fichier Ruby : Créez un nouveau fichier pour votre module Modbus Scanner dans le dossier approprié. Par exemple :

nano ~/.msf4/modules/auxiliary/scanner/scada/modbus_scanner.rb
Coller le code du module : Collez le code Ruby que vous avez modifié (le module de Modbus Scanner avec les UNIT_IDs automatiques) dans ce fichier. Voici le code :


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
Enregistrer le fichier :

Appuyez sur Ctrl + O pour sauvegarder le fichier, puis Enter pour confirmer.
Appuyez sur Ctrl + X pour quitter l'éditeur.
Étape 3 : Vérifier que le module est reconnu
Lancer Metasploit : Ouvrez un terminal sur votre Kali et lancez Metasploit :

bash
Copier le code
msfconsole
Charger le module personnalisé : Dans Metasploit, vous pouvez maintenant essayer de charger votre module personnalisé. Comme vous l'avez placé dans le répertoire ~/.msf4/modules/auxiliary/scanner/scada/, vous pouvez l'appeler directement :

bash
Copier le code
use auxiliary/scanner/scada/modbus_scanner
Configurer les options et lancer le module :

Configurez l'adresse IP de la cible (par exemple) :

set RHOSTS <target_ip>
Lancez le scan :

run


-> Résolution des problèmes
Si le module ne se charge pas correctement ou si vous rencontrez des problèmes, voici quelques étapes à suivre :

Vérifier le chemin :

Assurez-vous que le module est bien placé dans le répertoire correct :

~/.msf4/modules/auxiliary/scanner/scada/modbus_scanner.rb
Vérifier les permissions :

Assurez-vous que le fichier a les permissions correctes :

chmod 644 ~/.msf4/modules/auxiliary/scanner/scada/modbus_scanner.rb
Redémarrer Metasploit :

Si le module ne se charge pas, essayez de redémarrer Metasploit.
