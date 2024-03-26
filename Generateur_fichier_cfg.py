import json
import math

with open("config.json", 'r') as fichier:
    # Charger le contenu JSON dans une variable Python (ici, un dictionnaire)
    config = json.load(fichier)

def MasqueToAddress(masque) :
    address = ""
    masque = int(masque)
    for _ in range (4) :
        octet = 0
        for j in range(8) :
            if masque > 0 :
                octet += 2**(7-j)
                masque -= 1
        address += str(octet) + "."
    address = address[:-1]
    while len(address.split(".")) < 4 :
        address += ".0"
    return address

nombre_routers = 0
liste_AS = list(config.keys())
liste_AS = [e for e in liste_AS if e != "Route_map"] #la liste des numeros des AS
nombre_AS = len(liste_AS)

for i in range(nombre_AS):
    nombre_routers += int(config[liste_AS[i]]["Nombre_routeur"])

liste_clients = []
for i in range(nombre_AS) :
    if config[liste_AS[i]]["Type_AS"][:6] == "Client" and config[liste_AS[i]]["Type_AS"] not in liste_clients :
        liste_clients.append(config[liste_AS[i]]["Type_AS"])

for i in range(nombre_AS) : #on parcours chaque AS
    nombre_routers_AS = config[liste_AS[i]]["Nombre_routeur"] #le nombre de routers dans l'AS
    liste_router = [config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Dynamips_ID"] for j in range(nombre_routers_AS)] #liste des routers dans l'AS
    nombre_reseaux = 0

    if nombre_routers_AS > 0 :
        for j in range(1, nombre_routers_AS) :
            for k in range(j) :
                if config[liste_AS[i]]["Matrice_adjacence"][j][k] == 1 :
                    nombre_reseaux += 1

    for j in range(config[liste_AS[i]]["Nombre_routeur"]) : #on setup chaque router dans l'AS
        num_router = config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Dynamips_ID"] #le numero du router
        adresses_routers_remote = [] #liste des adresses des routers d'autres AS

        with open('fichiers_cfg/' + "R"+ str(num_router) +"_configs_i" + str(num_router) + "_startup-config.cfg",'w') as fichier_cfg :

            fichier_cfg.writelines(['!\n', 'hostname ' + config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Nom"] + '\n', '!\n'])

            ######### vrf definitions ########

            if config[liste_AS[i]]["Type_AS"] == "AS" :
                if str(j+1) in list(config[liste_AS[i]]["Routage_interAS"].keys()) :
                    for k in range(len(liste_clients)) :
                        fichier_cfg.writelines([
                            f"vrf definition {liste_clients[k]}\n",
                            f" rd 11{liste_AS[i]}:11{k+1}\n",
                            f" route-target export 11{liste_AS[i]}:100{k+1}\n",
                            f" route-target import 11{liste_AS[i]}:100{k+1}\n",
                            "!\n"
                        ])
                
                if config[liste_AS[i]]["Type_AS"] == "AS" :
                    fichier_cfg.writelines([
                        "mpls label protocol ldp\n",
                        "multilink bundle-name authenticated\n",
                        "!\n"
                    ])

            ######### loopback ########

            fichier_cfg.writelines([
                    "interface Loopback0\n",
                    " ip address 126.0.0." + str(num_router) + " " + str(MasqueToAddress(32)) + "\n"
            ])
            if config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "OSPF" : 
                fichier_cfg.writelines([
                    " ip ospf " + liste_AS[i] + " area " + liste_AS[i] + "\n",
                    " no shutdown\n"
                ])
            fichier_cfg.write("!\n")

            ######### interfaces ########

            for k in range(config[liste_AS[i]]["Nombre_routeur"]) : 
                if config[liste_AS[i]]["Matrice_adjacence"][j][k] == 1 : # S'il y a un lien on crée une interface
                    fichier_cfg.writelines([
                        "interface " + config[liste_AS[i]]["Matrice_adressage_interface"][j][k][1] + "\n",
                        " negotiation auto\n",
                        " ip address " + config[liste_AS[i]]["Matrice_adressage_interface"][j][k][0].split('/')[0] + " " + str(MasqueToAddress(config[liste_AS[i]]["Matrice_adressage_interface"][j][k][0].split('/')[1])) + "\n",
                        " mpls ip\n"
                    ])
                    if config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "OSPF" :
                        fichier_cfg.writelines([
                            " ip ospf " + liste_AS[i] + " area " + liste_AS[i] + " \n"
                        ])
                    fichier_cfg.write("!\n")

                    ######### interfaces entre les borders

            if str(j+1) in list(config[liste_AS[i]]["Routage_interAS"].keys()) : #si c'est un router de bordure
                for k in list(config[liste_AS[i]]["Routage_interAS"][str(j+1)].keys()) :
                    fichier_cfg.write("interface " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Interface"] + "\n")

                    if config[liste_AS[i]]["Type_AS"] == "AS" :
                        fichier_cfg.write(" vrf forwarding " + config[k]["Type_AS"] + "\n")

                    fichier_cfg.writelines([
                            " ip address " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Adresse"].split('/')[0] + " " + str(MasqueToAddress(config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Adresse"].split('/')[1])) + "\n",
                            " negotiation auto\n",
                            "!\n"
                        ])

            ######### routage bgp ########

            fichier_cfg.writelines([
                "router bgp " + "11" + liste_AS[i] + "\n",
                " bgp router-id " + 3*(str(num_router) + ".") + str(num_router) + "\n",
                " bgp log-neighbor-changes\n",
            ])

            if "Client" in config[liste_AS[i]]["Type_AS"] : #si c'est un client
                for k in list(config[liste_AS[i]]["Routage_interAS"][str(j+1)].keys()) :
                    num_router_remote = str(config[liste_AS[i]]["Routage_interAS"][str(j+1)][k]["Num_routeur_bordeur_remote"])
                    adresses_routers_remote.append(config[k]["Routage_interAS"][num_router_remote][str(i+1)]["Adresse"].split("/")[0])
                    fichier_cfg.writelines([
                        " neighbor " + adresses_routers_remote[-1] + " remote-as " + "11" + k + "\n"
                    ])

            for k in range(config[liste_AS[i]]["Nombre_routeur"] - 1) :
                fichier_cfg.writelines([
                    " neighbor 126.0.0." + str([e for e in liste_router if e != num_router][k]) + " remote-as " + "11" + liste_AS[i] + "\n",
                    " neighbor 126.0.0." + str([e for e in liste_router if e != num_router][k]) + " update-source Loopback0\n"
                ])

            fichier_cfg.write(" !\n")

                    ######### adresse-family ########
            
            if "Client" in config[liste_AS[i]]["Type_AS"] :
                fichier_cfg.writelines([
                    " address-family ipv4\n",
                    "  neighbor " + adresses_routers_remote[-1] + " activate\n",
                    " exit-address-family\n",
                    " !\n"
                ])

            else :
                fichier_cfg.write(" address-family vpnv4\n")
                for k in range(config[liste_AS[i]]["Nombre_routeur"] - 1) :
                    fichier_cfg.writelines([
                        "  neighbor 126.0.0." + str([e for e in liste_router if e != num_router][k]) + " activate\n"
                    ])
                fichier_cfg.write(" exit-address-family\n !\n")

                
                if str(j+1) in list(config[liste_AS[i]]["Routage_interAS"].keys()) : #s'il s'agit du router border, on configure le routage inter AS
                    for k in list(config[liste_AS[i]]["Routage_interAS"][str(j+1)].keys()) :
                        fichier_cfg.writelines([
                            " address-family ipv4 vrf " + config[k]["Type_AS"] + "\n",
                        ])
                        num_router_remote = str(config[liste_AS[i]]["Routage_interAS"][str(j+1)][k]["Num_routeur_bordeur_remote"])
                        adresses_routers_remote.append(config[k]["Routage_interAS"][num_router_remote][str(i+1)]["Adresse"].split("/")[0])
                        fichier_cfg.writelines([
                            "  neighbor " + adresses_routers_remote[-1] + " remote-as " + "11" + k + "\n",
                            "  neighbor " + adresses_routers_remote[-1] + " activate\n",
                            " exit-address-family\n"
                        ])
                        fichier_cfg.write(" !\n")

            if config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "OSPF" :
                fichier_cfg.writelines([
                    "router ospf " + liste_AS[i] + "\n",
                    " router-id " + 3*(str(num_router) + ".") + str(num_router) + "\n",
                    "!\n"
                ])

            ######### end ########           

            fichier_cfg.writelines([
                "end\n"
            ])
