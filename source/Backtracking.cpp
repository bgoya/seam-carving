#include "Backtracking.h"
#include "FuerzaBruta.h" // Para la función calcularEnergia

std::vector<int> encontrarSeamBacktracking_aux(const std::vector<std::vector<double>>& energia, std::vector<int> sol, double& opt) {
    int i = sol.size()-1;
    int j = sol[sol.size()-1];
    
    if(j < 0 || j >= energia[0].size()) {return {};} // Caso base 1: la posicion es invalida

    double energia_seam = calcularEnergia(energia, sol); 
    if(opt != -1 && energia_seam >= opt) {return {};} // Caso base 2 (poda): la solución no es optima
    
    if(i == energia.size()-1) { // Caso base 3: encontramos optimo
        opt = energia_seam;
        return sol;
    }

    sol.push_back(j-1);
    std::vector<int> s1 = encontrarSeamBacktracking_aux(energia, sol, opt);
    sol[sol.size()-1] = j;
    std::vector<int> s2 = encontrarSeamBacktracking_aux(energia, sol, opt);
    sol[sol.size()-1] = j+1;
    std::vector<int> s3 = encontrarSeamBacktracking_aux(energia, sol, opt);
    
    if(!s3.empty()) {
        return s3;
    } else if(!s2.empty()) {
        return s2;
    } else if(!s1.empty()) {
        return s1;
    }

    return {};
}

std::vector<int> encontrarSeamBacktracking(const std::vector<std::vector<double>>& energia) {
    // Cuento filas y columnas
    if (energia.empty()) {return {};}
    int m = energia[0].size();

    // Recorro la primera fila y llamo a la función recursiva
    std::vector<int> seam_opt;
    double energia_opt = -1;

    for(int i = 0; i < m; i++) {
        std::vector<int> seam_loc = encontrarSeamBacktracking_aux(energia, {i}, energia_opt);
        if(!seam_loc.empty()) {seam_opt = seam_loc;}
    }

    return seam_opt;
}
