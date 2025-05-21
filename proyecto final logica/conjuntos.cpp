#include <iostream>     // Para entrada/salida estándar
#include <set>          // Para usar conjuntos (set)
#include <string>       // Para manipular cadenas de texto
#include <fstream>      // Para manejar archivos
#include <map>          // Para almacenar múltiples conjuntos con nombres
#include <algorithm>    // Para funciones como remove_if
using namespace std;

// Función que verifica si un nombre de conjunto ya ha sido usado
bool nombre_usado(const map<string, set<string>>& conjuntos, const string& nombre) {
    return conjuntos.find(nombre) != conjuntos.end();
}

int main() {
    const int MAX_CONJUNTOS = 10;     // Número máximo de conjuntos permitidos
    const int MAX_ELEMENTOS = 15;    // Número máximo de elementos por conjunto

    map<string, set<string>> conjuntos; // Mapa para almacenar conjuntos con su nombre
    int numConjuntos;

    // Solicita al usuario cuántos conjuntos desea ingresar
    while (true) {
        cout << "¿Cuántos conjuntos deseas ingresar? (Máximo " << MAX_CONJUNTOS << "): ";
        cin >> numConjuntos;

        // Verifica que la entrada sea válida
        if (cin.fail() || numConjuntos < 1 || numConjuntos > MAX_CONJUNTOS) {
            cin.clear();             // Limpia el estado de error
            cin.ignore(1000, '\n');  // Descarta entrada incorrecta
            cout << "Entrada inválida. Ingresa un número entre 1 y " << MAX_CONJUNTOS << "." << endl;
        } else {
            cin.ignore();            // Limpia el buffer de entrada después del número
            break;
        }
    }

    // Funcion para ingresar cada conjunto
    for (int i = 0; i < numConjuntos; ++i) {
        string nombre;
        while (true) {
            cout << "\nNombre del conjunto #" << (i + 1) << ": ";
            getline(cin, nombre);

            // Verifica si el nombre ya fue usado
            if (nombre_usado(conjuntos, nombre)) {
                cout << "Este nombre ya fue utilizado. Usa un nombre único." << endl;
                continue;
            }

            cout << "Ingrese hasta " << MAX_ELEMENTOS << " elementos separados por comas para el conjunto " << nombre << ": ";
            string linea;
            getline(cin, linea);

            set<string> elementos;
            size_t start = 0, end;

            // Procesa la línea separando los elementos por comas
            while ((end = linea.find(',', start)) != string::npos) {
                string token = linea.substr(start, end - start);
                token.erase(remove_if(token.begin(), token.end(), ::isspace), token.end());
                if (!token.empty()) elementos.insert(token);
                start = end + 1;
            }

            // Agrega el último elemento
            string ultimo = linea.substr(start);
            ultimo.erase(remove_if(ultimo.begin(), ultimo.end(), ::isspace), ultimo.end());
            if (!ultimo.empty()) elementos.insert(ultimo);

            // Verifica que no exceda el límite de elementos
            if (elementos.size() > MAX_ELEMENTOS) {
                cout << "Has superado el límite de " << MAX_ELEMENTOS << " elementos. Intenta de nuevo." << endl;
                continue;
            }

            // Muestra el conjunto ingresado
            cout << "\nConjunto ingresado: " << nombre << " = { ";
            for (const auto& e : elementos) cout << e << " ";
            cout << "}" << endl;

            // Pide confirmación al usuario
            cout << "¿Deseas dejar este conjunto así? (s/n): ";
            string confirmar;
            getline(cin, confirmar);
            if (!confirmar.empty() && (confirmar[0] == 's' || confirmar[0] == 'S')) {

                conjuntos[nombre] = elementos;     // Guarda el conjunto
                break;
            } else {
                cout << "Reingresando los elementos del conjunto..." << endl;
            }
        }
    }

    // Muestra todos los conjuntos ingresados
    cout << "\nConjuntos ingresados:" << endl;
    for (const auto& par : conjuntos) {
        cout << par.first << " = { ";
        for (const auto& e : par.second) cout << e << " ";
        cout << "}" << endl;
    }

    // Guarda los conjuntos en un archivo de texto
    ofstream archivo("conjuntos.txt");
    for (const auto& par : conjuntos) {
        archivo << par.first << ":";          // Nombre del conjunto
        for (const auto& e : par.second) {
            archivo << e << ",";              // Elementos separados por coma
        }
        archivo << "\n";
    }

    cout << "\nConjuntos guardados en conjuntos.txt" << endl;
    return 0;
}