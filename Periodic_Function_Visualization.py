bl_info = {
    "name": "Python Application Numeri Primi",
    "author": "Douglas Ruffini",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Python Application Numeri Primi",
    "category": "Add Mesh",
}


import bpy
from bpy.props import BoolProperty


class EditorSwitcherMenu(bpy.types.Menu):
    #Shortcut menu
    #Menu a scelta rapida
    bl_idname = "editor_switcher_pie_menu"
    bl_label = "Numeri Primi"
    
    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator("object.import_numeri_primi",
        text="Import vertex",icon="VIEW3D").activate ="1"       
        pie.operator("object.import_numeri_primi",
        text="Join vertex to edges",icon="NODETREE").activate ="2"       
        pie.operator("object.import_numeri_primi",
        text="Join vertex to faces",icon="ACTION").activate ="3"
        pie.operator("object.import_numeri_primi",
        text="Vertex y & x long",icon="ACTION").activate ="5"
        pie.operator("object.import_numeri_primi",
        text="Vertex y & xz long",icon="ACTION").activate ="6"
        pie.operator("object.import_numeri_primi",
        text="Remuve vertex",icon="ACTION").activate ="4"
        pie.operator("object.import_numeri_primi",
        text="Periodic function  NP1",icon="ACTION").activate ="7"
        pie.operator("object.import_numeri_primi",
        text="Periodic function NP2",icon="ACTION").activate ="8"

class ultimoPrimo(bpy.types.Operator):

    bl_idname = "object.import_numeri_primi" 

    bl_label = "Import vertex"
    bl_label_two = "Join vertex to edges"
    bl_label_three = "Join vertex to faces"
    bl_label_four = "Remuve vertex"
    bl_label_five = "Vertex y & x long"
    bl_label_six = "Vertex y & xz long"
    bl_label_seven = "Periodic function NP1"
    bl_label_eight = "Periodic function NP2"

    hl_label = "Import vertex"
    hl_label_two = "Join vertex to edges"
    hl_label_three = "Join vertex to faces"
    hl_label_four = "Remuve vertex"
    hl_label_five = "Vertex y & x long"
    hl_label_six = "Vertex y & xz long"
    hl_label_seven = "Periodic function NP1"
    hl_label_eight = "Periodic function NP2"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Scalar or Vector Panel"
    bl_options = {'REGISTER', 'UNDO'}
    

    global verts_b
    verts_b = []
 
    global verts
    verts = []

    global edges
    edges = []

    global faces  
    faces = []

    global mesh
    mesh = None
  
    global obj
    obj = None

    global file_name
    file_name = ""  

    global ind
    ind =0

    global index
    index =0
    
    global array
    array= []

    #Set restrictions on the file dialog 
    #Impostare le restrizioni alla finestra di dialogo file
    filter_glob: bpy.props.StringProperty(default="*.txt", options = {'HIDDEN'})
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    some_boolean: BoolProperty( name='Do a thing', 
    description='Do a thing with the file you\'ve selected', default=True, )
    
    #Variable linked to the click of the object menu buttons
    #Variabile legata al click dei pulsanti menu oggetto
    activate: bpy.props.StringProperty(name="activate", description="activate")   


    #------------------------
    #Start your code function
    #Inizio delle tue funzioni 

    #Apri
    def apri_file(nome_file, s):
        f = open(nome_file, s) 
        return f

    #Leggi
    def leggi_file(f):
        return f.read()

    def leggi_parte_file(f, n):
        return f.read(n)
    
    def leggi_una_riga(f):
        return f.readline()

    #Esiste 
    def esiste(path, os):
        try:    
            return os.path.exists(path)

        except Exception as e:
            print("L'errore e' : ", e)

    def esiste_file(sorgente, os):      
        try:
            #Verifica la registrazione del path file
            #nomefile = os.environ.get(sorgente)
            #if nomefile and os.path.isfile(nomefile):
            return os.path.isfile(sorgente)

        except Exception as e:
            print("L'errore e' : ", e)

    def esiste_dir(direc, os):
        try:
            #Verifica la registrazione della directory
            #nomedir = os.environ.get(direc)
            #if nomedir and os.path.isdir(nomedir):
            return os.path.isdir(direc)

        except Exception as e:
            print("L'errore e' : ", e)

    #Elimina
    def elimina_file(f, os):
        bool_=False
        try:
            os.remove(f) 
            bool_ = True
            return bool_    

        except Exception as e:
            print("L'errore e' : ", e)
            return bool_ 

    def elimina_dir(c, os):
        bool_=False
        try:
            os.rmdir(c)  
            return bool_    

        except Exception as e:
            print("L'errore e' : ", e)
            return bool_       

    #Stampa
    def stampa_file(t):
        print(t)

    #Chiudi 
    def chiudi_file(f):
        try:
            f.close() 
            
        except Exception as e:
            print("L'errore e' : ", e)

    def preparaArray(f):

        global array
        array=[]
        s =f.split("\n")
 
        for riga in s:
            if riga !='':
                vector = riga.split(" ")
                a = ((vector[0]).replace(',', '.'))
                b = ((vector[1]).replace(',', '.'))
                c = ((vector[2]).replace(',', '.'))  
                d = ((vector[3]).replace(',', '.'))
                # Consider columns 2, 3, 4
                array.append([float(b), float(c), float(d)])
         
        return array

    def vertici(array):
        v = []
       
        for x in (array):
            v.append(x)  

        return v

    def lati(array):
        global edges
        edges = []
        edges = [[i, i+1] for i in range(len(array)-1)]

        return edges

    def facce_C(array, k):
        global verts_b
        global faces

        verts_b = []
        faces = []  
        h=0
        indice = 0
        linea = 0
        
        for i in array:
            if h<=k:
                linea = linea + i[1]
                
                verts_b.append( (linea, 0, 0) ) 
                verts_b.append( (0, i[1], 0) )
                verts_b.append( (0, 0, linea) )
                
                faces.append([indice, indice+1, indice+2])
                indice = indice + 3

            h = h+1

        return faces       

    def facce_B(array, k):
        global verts_b
        global faces

        verts_b = []
        faces = []  
        h=0
        indice = 0
        linea = 0
        
        for i in array:
            if h<=k:
                linea = linea + i[1]
                
                verts_b.append( (linea, 0, 0) ) 
                verts_b.append( (0, i[1], 0) )
                verts_b.append( (0, 0, 0) )
                
                faces.append([indice, indice+1, indice+2])
                indice = indice + 3

            h = h+1

        return faces       

    def facce(array, k):
        global verts_b
        global faces

        verts_b = []
        faces = []  
        h=0
        indice = 0
        
        for i in array:
            if h<=k:
                verts_b.append( (i[0], 0, 0) ) 
                verts_b.append( (0, i[1], 0) )
                verts_b.append( (0, 0, i[2]) )                   
                
            faces.append([indice, indice+1, indice+2])
            indice = indice + 3

            h = h+1

        return faces       
    
    def rimuoviMesh(bpy):
        #Removes the produced mesh
        #Rimuove la mesh prodotta
        global obj
        global file_name
        global array
        array=[]
    
  
        #if obj is not None:     
        #obj_data = obj.data
            #Remuve object
            #Rimuovo l'oggetto            
        #bpy.data.objects.remove(obj)
            #Then its data
            #Anche i suoi dati
        #bpy.data.meshes.remove(obj_data)   
            
        for o in bpy.data.objects: 
            if o.type == 'MESH':
                str=o.name
                if str.find("Primi")!= -1:
                    obj_data = o.data
                    bpy.data.objects.remove(o)
                    bpy.data.meshes.remove(obj_data)  
                    
        if bpy.data.collections.get("Collection"):
            collection_to_remove = bpy.data.collections.get('Collection')
            for object in collection_to_remove.objects:
                if (object.name !='Camera') or (object.name !='Light'):
                    str=object.name
                    if str.find("Primi")!= -1:
                        obj_data = object.data
                        bpy.data.objects.remove(object)
                        bpy.data.meshes.remove(obj_data)
                        
        obj=None
        file_name=""
        

        return obj

    #Find the periodic function
    #Trova la funzioni periodica
    def caricaFunzionePeriodica(bpy, array, os, k):
        import numpy as np
        import matplotlib.pyplot as plt

        global edges  
        global verts_b
        global faces

        edges = []
        verts_b = []
        faces = []  

        # We only use the 'Np1' column for simplicity in detecting the
        # periodicity.
        y_values = [item[k] for item in array]  # Colonna Np1

        if len(y_values) < 2:
            print("Dataset insufficiente per analizzare la periodicità.")
            return False

        # Fourier transform to analyze periodicity.
        y_fft = np.fft.fft(y_values)
        frequencies = np.fft.fftfreq(len(y_values))
        magnitudes = np.abs(y_fft)

        # Determine the dominant frequency (ignore the zero frequency)
        dominant_freq_idx = np.argmax(magnitudes[1:]) + 1
        dominant_freq = frequencies[dominant_freq_idx]

        # Checking the periodicity based on the dominant frequency.
        if dominant_freq != 0:
            period = abs(1 / dominant_freq)
            print(f"Frequenza dominante trovata: {dominant_freq:.4f},” + 
            “ periodo stimato: {period:.4f}")
            print("I dati mostrano un comportamento periodico.")
        else:
            print("Non è stata rilevata periodicità nei dati.")
    
        # Step 1: Generazione del Grafico e Salvataggio
        #image_path = '/tmp/sequenza_np1_grafico.png'  
        # Specify a path for the image
        # Replace with your preferred path
        output_dir = "C:/path/to/output/"
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)  
        image_path = os.path.join(output_dir, "sequenza_np1_grafico.png")

        plt.figure(figsize=(12, 6))
        plt.plot(y_values, marker='o', linestyle='-', color='b')
        plt.title("Sequenza di valori in 'y'")
        plt.xlabel("Indice")
        plt.ylabel("Valore")
        plt.grid()
        plt.savefig(image_path)
        plt.close()
 
 
        verts_b = [(i, y, 0) for i, y in enumerate(y_values)]  # (x, y, z)
        edges = [(i, i + 1) for i in range(len(verts_b) - 1)]
        
        return True   

    #These four functions are used by the dictionary     
    #Queste quattro funzioni servono al dizionario
    
    def azioneUno(self, bpy, os):
        global obj        
      
        if(ind=='1'):    
            if (file_name == ""):
                ultimoPrimo.rimuoviMesh(bpy)
                ultimoPrimo.associaArray(self, os)
            
            obj=ultimoPrimo.caricaMesh(bpy, ultimoPrimo.vertici(array), [], [])   

        return True
        

    def azioneDue(self, bpy, os):
        global obj        
        
        if (ind == '2'): 
            if(file_name == ""):
                ultimoPrimo.rimuoviMesh(bpy)
                ultimoPrimo.associaArray(self, os)

            obj=ultimoPrimo.caricaMesh(bpy, ultimoPrimo.vertici(array), 
            ultimoPrimo.lati(array), []) 

        return True
        

    def azioneTre(self, bpy, os):
        global obj        

        if (ind == '3'):
            if (file_name == ""):
                ultimoPrimo.rimuoviMesh(bpy)
                ultimoPrimo.associaArray(self, os)
            
            ultimoPrimo.facce(array, index)
            obj=ultimoPrimo.caricaMesh(bpy, verts_b, [], faces) 

        return True
        

    def azioneQuattro(bpy):
        global file_name
        
        if (ind == '4'):
            #If it exists then I remove object
            #Se esiste allora rimuovo oggetto
            if obj is not None:
                ultimoPrimo.rimuoviMesh(bpy)
            else:
                file_name="" 
            
            
    def azioneCinque(self, bpy, os):
        global obj        

        if (ind == '5'):
            if (file_name == ""):
                ultimoPrimo.rimuoviMesh(bpy)
                ultimoPrimo.associaArray(self, os)
            
            ultimoPrimo.facce_B(array, index)
            obj=ultimoPrimo.caricaMesh(bpy, verts_b, [], faces) 

        return True


    def azioneSei(self, bpy, os):
        global obj        

        if (ind == '6'):
            if (file_name == ""):
                ultimoPrimo.rimuoviMesh(bpy)
                ultimoPrimo.associaArray(self, os)
            
            ultimoPrimo.facce_C(array, index)
            obj=ultimoPrimo.caricaMesh(bpy, verts_b, [], faces) 

        return True
    
    def azioneSette(self, bpy, os):
        global obj        
        
        if (ind == '7'): 
            if(file_name == ""):
                ultimoPrimo.rimuoviMesh(bpy)
                ultimoPrimo.associaArray(self, os)

            ultimoPrimo.caricaFunzionePeriodica(bpy, array, os, 1) 
            obj=ultimoPrimo.caricaMesh(bpy, verts_b, edges, []) 

        return True

    def azioneOtto(self, bpy, os):
        global obj        
        
        if (ind == '8'): 
            if(file_name == ""):
                ultimoPrimo.rimuoviMesh(bpy)
                ultimoPrimo.associaArray(self, os)

            ultimoPrimo.caricaFunzionePeriodica(bpy, array, os, 2) 
            obj=ultimoPrimo.caricaMesh(bpy, verts_b, edges, []) 

        return True

    def caricaMesh(bpy, verts_, edges_, faces_ ):
        global mash
        mesh = None     
        global obj
        obj = None

        #Associa la mesh all'oggetto
        
        mesh = bpy.data.meshes.new("Primi")
        obj = bpy.data.objects.new("Primi",mesh)
        mat = bpy.data.materials.new(name="NewMaterial") 

        #Associa al materiale il colore Rosso 
        mat.diffuse_color = (1.0, 0.0, 0.0, 1.0) 

        #Aggiungi la proprietà all'oggetto
        obj.data.materials.append(mat)

        #Posiziona l'oggetto
        obj.location = (0,0,0) 

        #Ritorna la collezione dell'oggetto
        col = bpy.data.collections.get("Collection")
        col.objects.link(obj)

        #Associa la collezione alla scena
        bpy.context.view_layer.objects.active = obj

        #Proietta facce e vertici 
        mesh.from_pydata(verts_, edges_, faces_)

        return obj
               

    def associaArray(self, os):
        global index
        global array
        global file_name
        
        index = 0
        array = []

        file_name = self.filepath
        if file_name!="" or file_name!='':
            #il file e' nella directory del progetto
            if  ultimoPrimo.esiste(file_name, os):

                f=ultimoPrimo.apri_file(file_name, "r") 

                array= ultimoPrimo.preparaArray(ultimoPrimo.leggi_file( f ) )

                index = len(array)-1

                ultimoPrimo.chiudi_file(f)

    #End your code function
    #Fine delle tue funzioni
    #These two functions (execute, ivoke) are part of the plugin structure 
    #Queste due funzioni (execute, ivoke) fanno parte della struttura del plugin   
    
    @classmethod
    def poll(cls, context):
        return True
     
    def execute(self, context):
        import bpy
        import os
        global ind
            
        azione ={'1' : ultimoPrimo.azioneUno(self, bpy, os), 
        '2' : ultimoPrimo.azioneDue(self, bpy, os), 
        '3' : ultimoPrimo.azioneTre(self, bpy, os), 
        '4' : ultimoPrimo.azioneQuattro(bpy), 
        '5' : ultimoPrimo.azioneCinque(self, bpy, os) , 
        '6' : ultimoPrimo.azioneSei(self, bpy, os), 
        '7' : ultimoPrimo.azioneSette(self, bpy, os), 
        '8' : ultimoPrimo.azioneOtto(self, bpy, os)}     
          
        azione.get(ind)

        return {'FINISHED'}

    def invoke(self, context, event):        
        global file_name
        global ind

        #Check button number
        #Assegno numero pulsante  
          
        ind = self.activate
        
                                
        if (ind=='1' and  file_name == "") or (ind=='2' and file_name == "") \
        or (ind=='3' and file_name == "")  \
        or (ind=='5' and file_name == "") or (ind=='6' and file_name == "") \
        or (ind=='7' and file_name == "") or (ind=='8' and file_name == "") :  
            #Opens the file dialog
            #Apre la finestra di dialogo file
            context.window_manager.fileselect_add(self)
        else:
            return self.execute(context)
                                            
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    #This function create the voices in the menu object  
    #Questa funzione crea il menu oggetti e aggiunta di pulsanti sull'interfaccia utente
    self.layout.operator_context = 'INVOKE_DEFAULT'
    #Buttons present in the object menu  object  
    #Pulsanti presenti nel menu oggetto  
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.bl_label, 
    icon="VIEW3D").activate = "1"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.bl_label_two, 
    icon="NODETREE").activate="2"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.bl_label_three, 
    icon="ACTION").activate="3"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.bl_label_five, 
    icon="ACTION").activate="5"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.bl_label_six, 
    icon="ACTION").activate="6"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.bl_label_four, 
    icon="ACTION").activate="4"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.bl_label_seven, 
    icon="ACTION").activate="7"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.bl_label_eight, 
    icon="ACTION").activate="8"

def menu_header(self, context):
    #This function create the buttons in the ui
    #Questa funzione crea i pulsanti sull'interfaccia utente
    #Buttons present in the in the UI
    #Pulsanti presenti presenti nella UI 
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.hl_label, 
    icon="VIEW3D").activate = "1"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.hl_label_two, 
    icon="NODETREE").activate="2"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.hl_label_three, 
    icon="ACTION").activate="3"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.hl_label_five, 
    icon="ACTION").activate="5"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.hl_label_six, 
    icon="ACTION").activate="6"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.hl_label_four, 
    icon="ACTION").activate="4"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.hl_label_seven, 
    icon="ACTION").activate="7"
    self.layout.operator(ultimoPrimo.bl_idname, text =ultimoPrimo.hl_label_eight, 
    icon="ACTION").activate="8"

#Store keymaps 
#Memorizza le mappe dei tasti 
addon_keymaps = []
            
 
def register():
    #This function register the class
    #Questa funzione registra la classe 
    #Handle the keymap
    #Gestisci la mappa dei tasti
    wm = bpy.context.window_manager
    
    #Note that in background mode (no GUI available), keyconfigs are not available 
    #either,
    #so we have to check this to avoid nasty errors in background case.
    #Tieni presente che in modalità background (nessuna GUI disponibile), 
    #nemmeno i keyconfig sono disponibili,
    #quindi dobbiamo verificarlo per evitare errori spiacevoli nel caso in background.
    kc = wm.keyconfigs.addon
    
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name = 
        "Window",space_type='EMPTY', region_type='WINDOW')
        kmi = km.keymap_items.new("wm.call_menu_pie",
        type = "E",alt=True, value = "PRESS")
        kmi.properties.name = "editor_switcher_pie_menu" 
        addon_keymaps.append(km)
    
    bpy.utils.register_class(ultimoPrimo)
    bpy.utils.register_class(EditorSwitcherMenu)
    #Append
    #Aggiungi dopo
    bpy.types.VIEW3D_MT_object.append(menu_func)
    #Prepend
    #Aggiungi prima
    bpy.types.VIEW3D_HT_header.prepend(menu_header)
    

def unregister():
    #This function unregister the class
    #Questa funzione deregistra la classe
    #Note: when unregistering, it's usually good practice to do it in reverse order you 
    #registered.
    #Can avoid strange issues like keymap still referring to operators already 
    #unregistered...
    #Nota: quando si annulla la registrazione, di solito è buona norma farlo 
    #nell'ordine inverso a quello della registrazione.
    #Puù evitare problemi strani come la mappatura dei tasti che si riferisce ancora a 
    #operatori giù non registrati...
    #Handle the keymap
    #Gestisci la mappa dei tasti
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()
    
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.types.VIEW3D_HT_header.remove(menu_header)
    bpy.utils.unregister_class(EditorSwitcherMenu)
    bpy.utils.unregister_class(ultimoPrimo)
     

if __name__ == "__main__":
    register()
