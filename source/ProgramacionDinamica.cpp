#include "ProgramacionDinamica.h"

using namespace std;

double encontrarSeamPD_aux(const vector<vector<double>>& energia, vector<vector<double>>& memoizacion,int i, int j) {
    int n = energia.size();
    int m = energia[0].size();

    if (j < 0 || j >= m){return 1e18;} // Caso base 1: la posicion es invalida

    if (memoizacion[i][j] != -1.0){return memoizacion[i][j];} // Caso base 2 (pd): subproblema ya resuelto

    if (i == n - 1) { // Caso base 3: llegamos a la ultima fila
        memoizacion[i][j] = energia[i][j];
        return memoizacion[i][j];
    }

    double s1 = encontrarSeamPD_aux(energia, memoizacion, i + 1, j - 1);
    double s2 = encontrarSeamPD_aux(energia, memoizacion, i + 1, j);
    double s3 = encontrarSeamPD_aux(energia, memoizacion, i + 1, j + 1);

    memoizacion[i][j] = energia[i][j] + min(s1, min(s2, s3));
    return memoizacion[i][j];
}

vector<int> encontrarSeamPD(const vector<vector<double>>& energia) {
    // Cuento filas y columnas    
    int n = energia.size();
    if(!n) return {};
    int m = energia[0].size();

    // Tabla de memoización
    vector<vector<double>> memoizacion(n, vector<double>(m, -1.0));

    // A diferencia de fb y bt, trabajamos sobre columnas y no seams enteros
    // (justificacion cambio de aproach en el informe)
    int min_col = 0;
    for(int j = 0; j < m; j++) {
        encontrarSeamPD_aux(energia, memoizacion, 0, j);
        if(memoizacion[0][j] < memoizacion[0][min_col])
            min_col = j;
    }

    // Reconstruimos el seam
    vector<int> seam_opt(n);
    seam_opt[0] = min_col;
    for(int i = 1; i < n; i++) {
        int col = seam_opt[i-1];
        int energia_opt = col;
        if (col > 0 && memoizacion[i][col-1] < memoizacion[i][energia_opt]) energia_opt = col - 1;
        if (col < m - 1 && memoizacion[i][col+1] < memoizacion[i][energia_opt]) energia_opt = col + 1;
        seam_opt[i] = energia_opt;
    }

    return seam_opt;
}
