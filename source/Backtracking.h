#pragma once

#include <vector>

std::vector<int> encontrarSeamBacktracking(const std::vector<std::vector<double>>& energia);

std::vector<int> encontrarSeamBacktracking_aux(const std::vector<std::vector<double>>& energia, std::vector<int> sol, double& opt);
