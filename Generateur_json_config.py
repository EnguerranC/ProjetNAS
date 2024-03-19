import json

""" 
                                                ----------------------------------
                                                --- Generateur du fichier json ---
                                                ----------------------------------

L'essentiel des informations doivent être changées ou rajoutées à la main dans le dico config. Se réferer au Readme pour comprendre sa structure.
Pour rajouter un AS, rajouter juste l'AS et ses caractéristiques dans le dico config et modifier les autres AS pour les éventuels liens.

"""

# Generateur d'une matrice d'adressage vide
def Matrice_addressage_vide(M_ad, N) :
   for i in range(N) :
      M_temp = []
      for j in range(N) :
         M_temp.append(["",""])
      M_ad.append(M_temp)
   return M_ad

# Dictionnaire config à la base de la structure du fichier json
config = {
   1 : { # Numero de l'AS
      "Nombre_routeur" : 4, # Nombre de routeur dans l'AS
      "Type_AS" : "AS", # Type de l'AS (AS, Client, Peer ou Provider)
      "Matrice_adjacence" : [[0,1,0,0],
                             [1,0,1,0],
                             [0,1,0,1],
                             [0,0,1,0]],
      "Masque_reseau" : "111::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 4),
      "Donnees_routeurs" : { 
      },
      "Routage_intraAS" : { # Infos concernant le routage intraAS
         "Protocol" : "RIPng" 
      },
      "Routage_interAS":{ # Infos concernant le routage interAS
         3 : { # Numero du routeur bordeur
            2 : { # Numero de l'AS remote
               "Num_routeur_bordeur_remote" : 3, # Numero du routeur remote
               "Adresse" : "", # Adresse de l'interface liée au routeur remote
               "Interface" : "" # Interface liée au routeur remote
            }
         },
         2 : {
            3 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : "",
               "Interface" : ""
            }
         },
         1 : {
            4 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : "",
               "Interface" : ""
            }
         },
         4 : {
            5 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : "",
               "Interface" : ""
            }
         }
      },
   },
   2 : {
      "Nombre_routeur" : 4,
      "Type_AS" : "AS",
      "Matrice_adjacence" : [[0,1,0,0],
                             [1,0,1,0],
                             [0,1,0,1],
                             [0,0,1,0]],
      "Masque_reseau" : "112::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 4),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "OSPF"
      },
      "Routage_interAS":{
         3 : {
            1 : {
               "Num_routeur_bordeur_remote" : 3,
               "Adresse" : "",
               "Interface" : ""
            }
         },
         2 : {
            3 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : "",
               "Interface" : ""
            }
         },
         1 : {
            6 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : "",
               "Interface" : ""
            }
         }
      }
   },
   3 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "provider",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "113::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : ""
      },
      "Routage_interAS":{
         1 : {
            2 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : "",
               "Interface" : ""
            },
            1 : {
               "Num_routeur_bordeur_remote" : 2,
               "Adresse" : "",
               "Interface" : ""
            }
         }         
      }
   },
   4 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "peer",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "114::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : ""
      },
      "Routage_interAS":{
         1 : {
            1 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : ""
            }
         }
      }
   },
   5 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "client",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "115::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : ""
      },
      "Routage_interAS":{
         1 : {
            1 : {
               "Num_routeur_bordeur_remote" : 4,
               "Adresse" : "",
               "Interface" : ""
            }
         }
      }
   },
   6 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "client",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "116::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : ""
      },
      "Routage_interAS":{
         1 : {
            2 : {
               "Num_routeur_bordeur_remote" : 2,
               "Adresse" : "",
               "Interface" : ""
            }
         }
      }
   },
   "Route_map" : { # Infos concernant les routes map
         "fromprovider" : { # Nom de la route map
            "Prio" : 20, # Priorité de la route map
            "Set_community" : "Provider", # Communauté associée à la route map
            "Local_pref" : 50, # Local pref associé à la route map
            "Match_community" : None # Condition de match a une communauté
         },
         "toprovider" : {
            "Prio" : 20,
            "Set_community" : None,
            "Local_pref" : None,
            "Match_community" : "Client"
         },
         "frompeer" : {
            "Prio" : 20,
            "Set_community" : "Peer",
            "Local_pref" : 100,
            "Match_community" : None
         },
         "topeer" : {
            "Prio" : 20,
            "Set_community" : None,
            "Local_pref" : None,
            "Match_community" : "Client"
         },
         "fromclient" :{
            "Prio" : 20,
            "Set_community" : "Client",
            "Local_pref" : 150,
            "Match_community" : None
         },
         "toclient" : {
            "Prio" : 20,
            "Set_community" : None,
            "Local_pref" : None,
            "Match_community" : "Everybody"
            
         }
      },
}
"""
Generateur de la base de donnee des routeurs : Num_routeur, Nom, Dynamips_ID
Num_routeur : unique dans chaque AS (qui va de 1 à Nombre_routeur)
Nom : unique a tous les routeurs du reseau global et a pour forme AS[Num_AS]_R[Num_routeur]
Dynamips_ID : unique a tous les routeurs du reseau global
"""
Dynamips_ID = 1
for i in range(1,len(config)) :
   for j in range(1, config[i]["Nombre_routeur"]+1) :
      Num_routeur = j
      config[i]["Donnees_routeurs"][Num_routeur] = {"Nom":"AS"+str(i)+"_R"+str(j) , "Dynamips_ID":Dynamips_ID  , "Attributs":""}
      Dynamips_ID = Dynamips_ID +1

""" 
Fonction Adressage_AS(Nom_As, Matrice_adjacence, Nombre_routeur) --> None
Configure les adresses et les interfaces des liens d'une AS et inter AS dans le fichier json
Pour trouver les interfaces d'un routeur d'une AS il suffit de lire la ligne correspondant à son numero dans la matrice d'adressage de l'AS
"""
def Adressage_AS(Num_AS , Matrice_adjacence, Nombre_routeur) :
   nb_connexions = [0 for i in range(Nombre_routeur)]
   for routeur in range(Nombre_routeur) :
      for lien in range(routeur,Nombre_routeur) :
         if Matrice_adjacence[routeur][lien] :
            nb_connexions[routeur]+=1
            nb_connexions[lien]+=1
            interface1 = "GigabitEthernet" + str(nb_connexions[routeur]) + "/0"
            interface2 = "GigabitEthernet" + str(nb_connexions[lien]) + "/0"

            adresse_unique1 = config[Num_AS]["Masque_reseau"][:3]+":0:0:"+str(routeur+1)+"::"+"1/64"
            adresse_unique2 = config[Num_AS]["Masque_reseau"][:3]+":0:0:"+str(routeur+1)+"::"+"2/64"
            config[Num_AS]["Matrice_adressage_interface"][routeur][lien] = [adresse_unique1,interface1]
            config[Num_AS]["Matrice_adressage_interface"][lien][routeur] = [adresse_unique2, interface2]
      routeur+=1
      if routeur in list(config[Num_AS]["Routage_interAS"].keys()) :
         for remote_AS in list(config[Num_AS]["Routage_interAS"][routeur].keys()) :
            nb_connexions[routeur-1]+=1
            config[Num_AS]["Routage_interAS"][routeur][remote_AS]["Interface"] = "GigabitEthernet" + str(nb_connexions[routeur-1]) + "/0"
            if Num_AS > remote_AS :
               config[Num_AS]["Routage_interAS"][routeur][remote_AS]["Adresse"] = "2000:"+str(Num_AS)+str(remote_AS)+"::"+str(Num_AS)+"/32"
            else :
               config[Num_AS]["Routage_interAS"][routeur][remote_AS]["Adresse"] = "2000:"+str(remote_AS)+str(Num_AS)+"::"+str(Num_AS)+"/32"

"""
Programme principal
"""
for i in range(len(config)-1) :
   Adressage_AS(i+1, config[i+1]["Matrice_adjacence"], config[i+1]["Nombre_routeur"])

fichier = open("config.json","w") # Creation du fichier json
json.dump(config, fichier, indent=4)
