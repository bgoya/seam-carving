#pragma once

#include <vector>

std::vector<int> encontrarSeamFuerzaBruta(const std::vector<std::vector<double>>& energia);

std::vector<int> encontrarSeamFuerzaBruta_aux(const std::vector<std::vector<double>>& energia, std::vector<int> sol, double& opt);

double calcularEnergia(const std::vector<std::vector<double>>& energia, std::vector<int> seam);