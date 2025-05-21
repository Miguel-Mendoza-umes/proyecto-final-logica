#include <iostream>
#include <set>
#include <string>
#include <fstream>
#include <map>
#include <algorithm>
using namespace std;

bool nombre_usado(const map<string, set<string>>& conjuntos, const string& nombre) {
    return conjuntos.find(nombre) != conjuntos.end();
}

int main() {
    const int MAX_CONJUNTOS = 10;
    const int MAX_ELEMENTOS = 15;

    map<string, set<string>> conjuntos;
    int numConjuntos;

    while (true) {
        cout << "¿Cuántos conjuntos deseas ingresar? (Máximo " << MAX_CONJUNTOS << "): ";
        cin >> numConjuntos;
        if (cin.fail() || numConjuntos < 1 || numConjuntos > MAX_CONJUNTOS) {
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "Entrada inválida. Ingresa un número entre 1 y " << MAX_CONJUNTOS << "." << endl;
        } else {
            cin.ignore(); 
            break;
        }
    }

    for (int i = 0; i < numConjuntos; ++i) {
        string nombre;
        while (true) {
            cout << "\nNombre del conjunto #" << (i + 1) << ": ";
            getline(cin, nombre);

            if (nombre_usado(conjuntos, nombre)) {
                cout << "Este nombre ya fue utilizado. Usa un nombre único." << endl;
                continue;
            }

            cout << "Ingrese hasta " << MAX_ELEMENTOS << " elementos separados por comas para el conjunto " << nombre << ": ";
            string linea;
            getline(cin, linea);

            set<string> elementos;
            size_t start = 0, end;
            while ((end = linea.find(',', start)) != string::npos) {
                string token = linea.substr(start, end - start);
                token.erase(remove_if(token.begin(), token.end(), ::isspace), token.end());
                if (!token.empty()) elementos.insert(token);
                start = end + 1;
            }
            string ultimo = linea.substr(start);
            ultimo.erase(remove_if(ultimo.begin(), ultimo.end(), ::isspace), ultimo.end());
            if (!ultimo.empty()) elementos.insert(ultimo);

            if (elementos.size() > MAX_ELEMENTOS) {
                cout << "Has superado el límite de " << MAX_ELEMENTOS << " elementos. Intenta de nuevo." << endl;
                continue;
            }

            cout << "\nConjunto ingresado: " << nombre << " = { ";
            for (const auto& e : elementos) cout << e << " ";
            cout << "}" << endl;

            cout << "¿Deseas dejar este conjunto así? (s/n): ";
            string confirmar;
            getline(cin, confirmar);
            if (!confirmar.empty() && (confirmar[0] == 's' || confirmar[0] == 'S')) {
                conjuntos[nombre] = elementos;
                break;
            } else {
                cout << "Reingresando los elementos del conjunto..." << endl;
            }
        }
    }

    cout << "\nConjuntos ingresados:" << endl;
    for (const auto& par : conjuntos) {
        cout << par.first << " = { ";
        for (const auto& e : par.second) cout << e << " ";
        cout << "}" << endl;
    }

    ofstream archivo("conjuntos.txt");
    for (const auto& par : conjuntos) {
        archivo << par.first << ":";
        for (const auto& e : par.second) {
            archivo << e << ",";
        }
        archivo << "\n";
    }

    cout << "\nConjuntos guardados en conjuntos.txt" << endl;
    return 0;
}