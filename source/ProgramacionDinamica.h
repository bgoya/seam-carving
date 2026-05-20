#pragma once

#include <vector>

std::vector<int> encontrarSeamPD(const std::vector<std::vector<double>>& energia);

double encontrarSeamPD_aux(const std::vector<std::vector<double>>& energia, std::vector<std::vector<double>>& memoizacion,int i, int j);
