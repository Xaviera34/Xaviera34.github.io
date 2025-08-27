import tkinter as tk
from tkinter import messagebox
import math

# Datos: Z, símbolo, grupo, periodo, categoría, valencia aproximada (simplificada)
element_data = [
    (1,"H",1,1,"no_metal",1),(2,"He",18,1,"no_metal",0),
    (3,"Li",1,2,"metal",1),(4,"Be",2,2,"metal",2),(5,"B",13,2,"metaloide",3),(6,"C",14,2,"no_metal",4),
    (7,"N",15,2,"no_metal",3),(8,"O",16,2,"no_metal",2),(9,"F",17,2,"no_metal",1),(10,"Ne",18,2,"no_metal",0),
    (11,"Na",1,3,"metal",1),(12,"Mg",2,3,"metal",2),(13,"Al",13,3,"metal",3),(14,"Si",14,3,"metaloide",4),
    (15,"P",15,3,"no_metal",3),(16,"S",16,3,"no_metal",2),(17,"Cl",17,3,"no_metal",1),(18,"Ar",18,3,"no_metal",0),
    (19,"K",1,4,"metal",1),(20,"Ca",2,4,"metal",2),(31,"Ga",13,4,"metal",3),(32,"Ge",14,4,"metaloide",4),
    (33,"As",15,4,"metaloide",3),(34,"Se",16,4,"no_metal",2),(35,"Br",17,4,"no_metal",1),(36,"Kr",18,4,"no_metal",0)
]

# Convertir en diccionario
elements_by_symbol = {e[1]:{"Z":e[0],"simbolo":e[1],"grupo":e[2],"periodo":e[3],
                            "categoria":e[4],"val":e[5]} for e in element_data}

# Funciones para determinar funcionalidad
def es_metal_funcional(e):
    return e["grupo"] in (1,2,13) or e["simbolo"]=="H"  # IA, IIA, IIIA y H

def es_no_metal_funcional(e):
    return e["grupo"] in (14,15,16,17,18) and e["categoria"]!="metal"

seleccion = []

def formula_ionica(m_sym, nm_sym):
    m = elements_by_symbol[m_sym]
    nm = elements_by_symbol[nm_sym]
    if nm["val"] == 0:
        return None, f"{nm_sym} es gas noble, normalmente no reacciona."
    val_m, val_nm = abs(m["val"]), abs(nm["val"])
    mcm = math.lcm(val_m, val_nm)
    sub_m, sub_nm = mcm//val_m, mcm//val_nm
    return f"{m_sym}{sub_m if sub_m>1 else ''}{nm_sym}{sub_nm if sub_nm>1 else ''}", f"{m_sym}(+{val_m}) con {nm_sym}(-{val_nm})"

def on_click(sym):
    if len(seleccion) == 2:
        seleccion.clear()
        res_text.delete("1.0","end")
    seleccion.append(sym)
    sel_label.config(text="Seleccionado: "+", ".join(seleccion))
    if len(seleccion)==2:
        procesar()

def procesar():
    a,b = seleccion
    ea, eb = elements_by_symbol[a], elements_by_symbol[b]
    metal, nometal = None, None
    if es_metal_funcional(ea) and es_no_metal_funcional(eb): metal, nometal = a,b
    elif es_metal_funcional(eb) and es_no_metal_funcional(ea): metal, nometal = b,a
    else:
        res_text.insert("1.0","Debes elegir UN elemento IA/IIA/IIIA o H y UN no metal IVA-VIIIA.\n")
        seleccion.clear(); sel_label.config(text="Seleccionado: -")
        return
    formula, razon = formula_ionica(metal, nometal)
    res_text.delete("1.0","end")
    if formula: res_text.insert("1.0",f"Reacción: {metal} + {nometal} → {formula}\n{razon}")
    else: res_text.insert("1.0",razon)
    seleccion.clear(); sel_label.config(text="Seleccionado: -")

root = tk.Tk()
root.title("Tabla periódica organizada con grupos funcionales")

tk.Label(root, text="Haz clic en un elemento funcional (IA/IIA/IIIA o H) y un no metal (IVA-VIIIA):").grid(row=0, column=0, columnspan=18)

# Crear botones según posición real
for e in elements_by_symbol.values():
    r, c = e["periodo"], e["grupo"]
    color = "lightgray"
    if es_metal_funcional(e): color="lightblue"  # Metales funcionales y H
    if es_no_metal_funcional(e): color="lightgreen"  # No metales funcionales
    tk.Button(root, text=e["simbolo"], width=5, height=2, bg=color,
              command=lambda s=e["simbolo"]: on_click(s)).grid(row=r, column=c, padx=2, pady=2)

sel_label = tk.Label(root,text="Seleccionado: -"); sel_label.grid(row=8,column=0,columnspan=18)
res_text = tk.Text(root,height=5,width=60); res_text.grid(row=9,column=0,columnspan=18)

root.mainloop()
