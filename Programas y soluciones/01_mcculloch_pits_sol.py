import numpy as np

def neuronaMyP(E,I,u):
    for inhibitoria in I:
        if inhibitoria == 1:
            return 0
    
    integracion = 0
    for exitatoria in E:
        integracion = integracion + 1
    
    if integracion >= u:
        return 1
    else:
        return 0

def main():
    print("Neurona de McCulloch y Pitts!")
    # suponga 
    E = [1]
    print("E: ", E)
    I = [0]
    print("I: ", I)
    u = 1
    print("u: ", u)
    
    print("Resultado: ", neuronaMyP(E,I,u))


if __name__ == "__main__":
    main()