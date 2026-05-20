#include "FuerzaBruta.h"

double calcularEnergia(const std::vector<std::vector<double>>& energia, std::vector<int> seam) {
    double res = 0;
    for(int i = 0; i < seam.size(); i++) {
        res += energia[i][seam[i]];
    }
    return res;
}

std::vector<int> encontrarSeamFuerzaBruta_aux(const std::vector<std::vector<double>>& energia, std::vector<int> sol, double& opt) {
    int i = sol.size()-1;
    int j = sol[sol.size()-1];
    
    if(j < 0 || j >= energia[0].size()) {return {};} // Caso base 1: la posicion es invalida
    
    if(i == energia.size()-1) { // Caso base 2: llegamos a la ultima fila
        double energia_seam = calcularEnergia(energia, sol);
        if(opt == -1 || energia_seam < opt) {
            opt = energia_seam;
            return sol;
        }
        return {};
    }

    sol.push_back(j-1);
    std::vector<int> s1 = encontrarSeamFuerzaBruta_aux(energia, sol, opt);
    sol[sol.size()-1] = j;
    std::vector<int> s2 = encontrarSeamFuerzaBruta_aux(energia, sol, opt);
    sol[sol.size()-1] = j+1;
    std::vector<int> s3 = encontrarSeamFuerzaBruta_aux(energia, sol, opt);
    
    if(!s3.empty()) {
        return s3;
    } else if(!s2.empty()) {
        return s2;
    } else if(!s1.empty()) {
        return s1;
    }

    return {};
}

std::vector<int> encontrarSeamFuerzaBruta(const std::vector<std::vector<double>>& energia) {
    // Cuento filas y columnas
    if (energia.empty()) {return {};}
    int m = energia[0].size();

    // Recorro la primera fila y llamo a la función recursiva
    std::vector<int> seam_opt;
    double energia_opt = -1;

    for(int i = 0; i < m; i++) {
        std::vector<int> seam_loc = encontrarSeamFuerzaBruta_aux(energia, {i}, energia_opt);
        if(!seam_loc.empty()) {seam_opt = seam_loc;}
    }

    return seam_opt;
}