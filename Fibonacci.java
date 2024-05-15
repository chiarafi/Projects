//////////////////////////
//Informatik II - SoSe 2020
//Task 4.1. a
//////////////////////////

//////////////////////////
// Submission by:
// 
//  Chiara Fischer
//
//////////////////////////

public class Fibonacci {

	//////////////////////
	// Main function
	public static void main(String[] args) {
        //////////////////////
		// Task 4.1.a)
		// We print the first 10 numbers of the fibonacci sequence to check if
		// the implementation is correct. The output of all four functions 
		// should match the numbers of the fibonacciSequence array.
		long fibonacciSequence[] = {1, 1, 2, 3, 5, 8, 13, 21, 34, 55};
		for(long n = 1; n <= 10; n++) { 
            System.out.println("reference: " + fibonacciSequence[(int)(n-1)]);
            System.out.println("recursive: " + fibonacciRecursive(n)); 
            System.out.println("iterative: " + fibonacciIterative(n)); 
            System.out.println("power d&c: " + fibonacciPowerDC(n)); 
            System.out.println("matrixd&c: " + fibonacciPowerDCMatrix(n)); 
            System.out.println("------------------------"); 
        }
		
        //////////////////////
        // Task 4.1.b)
		//analzyeTimeComplexity();
	}
	
	//////////////////////
	// Task 4.1.a)
	// Implement the recursive version of the fibonacci sequence as stated in
	// the exam sheet.
	public static long fibonacciRecursive(long n) {
	    if(n==0) {return 0;} // Basisfall (dient auch Temrinierung)
	    if(n==1) {return 1;} // Basisfall (dient auch Temrinierung)
	    if(n>1) {return (fibonacciRecursive(n-1)+ fibonacciRecursive(n-2));} // Funktion rekursiv entsprechend der
	    // Definition für den Fibonacciwert von n aufrufen
		return -1; // Fall abfangen, falls n<0
	}
	
	//////////////////////
	// Task 4.1.a)
	// Implement the iterative version of the fibonacci sequence as stated in
	// the exam sheet.
	public static long fibonacciIterative(long n) {
		if(n==0) { // Basisfall (dient auch Terminierung)
			return 0;
		}
		if(n==1) {  // Basisfall (dient auch Terminierung)
			return 1;
		}
		int fib0 = 0; // Fibonacciwert für n=0
		int fib1 = 1; //Fibonacciwert für n=1
		// auf diesen Werten wird iterativ aufgebaut, bis der Fibonacciwert für das n erreicht wird 
		for(int i=2; i<=n; i++) {
			int fib2 = fib0+fib1;
			fib0=fib1;
			fib1=fib2;
		}
		return fib1;
	}
	
	//////////////////////
	// Task 4.1.a)
	// Implement the fibonacci sequence based on the power d&c function as 
	// stated in the exam sheet.
	public static long fibonacciPowerDC(long n) {
		
        return Math.round((Power_DC(((1+Math.sqrt(5))/2),n))/Math.sqrt(5)); /*hier rufe ich die Power_DC-Funktion auf und übergebe
        dieser den Wert des goldenen Schnitts und das n 
        das Ergebnis dessen teile ich durch die Wurzel von 5 und runde dies, da es während des Potenzierens zu numerischen
        Ungenauigkeiten kommen kann */
		
		
	}
	
	
	// Hilfsfunktion, die  einen Wert a mit dem Wert n potenziert 
	public static double Power_DC(double a,long n) {
		if(n==1) {return a;}
		else {
			double tmp = Power_DC(a,n/2);
			if(n%2==0) {
				return tmp*tmp;
			} else {
				return tmp*tmp*a;
			}
		}
		
	}
	
	//////////////////////
	// Task 4.1.a)
	// Implement the fibonacci sequence based on the power d&c function for 
	// 2x2 matrices as stated in the exam sheet.
	public static long fibonacciPowerDCMatrix(long n) {
		int[][] matrix = {{1,1}, {1,0}}; // Erstellung und Initialisierung der Matrix
		int[][] result = matrixPower_DC(matrix,n);  // mithilfe der matrixPower_DC - Funktion wird die Matrix mit n potenziert
		return result[0][1]; // der Eintrag oben rechts der Matrix beinhaltet den Wert fibonacci(n) und wird zurückgegeben
		
		
	}
	
	// Hilfsfunktion für das Potenzieren einer Matrix 
	public static int[][] matrixPower_DC(int[][] m, long n) {
		if(n==1) {return m;} // falls n=1 Matrix zurückgeben
		else { // für n>1:
			int[][] tmp = matrixPower_DC(m,n/2); // die Funktion  ruft sich rekusriv auf und halbiert dabei die Potenz (Divide&Conqer-Ansatz)
			// und das Ergebnis wird unter tmp gespeichert
			if(n%2==0) { // falls n gerade, multipliziere das Teilergebnis tmp mit sich selbst
				return multiply(tmp,tmp);
			}
			else { // falls n ungerade, multipliziere das Teilergebnis tmp mit sich selbst und einmal zusätzlich mit der ursprünglichen
				// Matrix m, um auf die ungerade Potenz zu kommen
				return multiply((multiply(tmp,tmp)),m);
			}
		}
	}
	
	// Hilfsfunktion für das Multiplizieren von 2 Matrizen
	 public static int[][] multiply(int[][] m1, int[][] m2) {
	    	int[][] result = new int[m1.length][m1.length];
	    	for(int i=0; i<m1.length; i++) {
	    		for(int j=0; j<m1.length; j++) {
	    			result[i][j] =0;
	    			for(int k=0; k<m1.length; k++) {
	    				result[i][j]+= m1[i][k] * m2[k][j];
	    			}
	    			
	    		}
	    	}
	    	return result;
	    }
    
	 
//////////////////////
// Task 4.1.b)
// Implement a function to measure and print the runtime of all four
// fibonacci algorithms.
public static void analzyeTimeComplexity() {
// TODO

int nMax = 50000;
int nMin = 1000;
int step = 1;

for(int n=nMin; n<=nMax; n+=step) {


// Laufzeit der rekursiven Funktion
long start = System.currentTimeMillis();
fibonacciRecursive(n);
long end= System.currentTimeMillis();
long timeRekursiv = end-start;

// Laufzeit der iterativ Funktion
long startIterativ = System.currentTimeMillis();
fibonacciIterative(n);
long endIterativ = System.currentTimeMillis();
long timeIterativ = endIterativ-startIterativ;

// Laufzeit der Funktion mit Ansatz des goldenen Schnitts
long startDC = System.currentTimeMillis();
fibonacciPowerDC(n);
long endDC = System.currentTimeMillis();
long timeDC = endDC-startDC;

// Laufzeit der Funktion mit Ansatz dere Matrizen
long startMatrix = System.currentTimeMillis();
fibonacciPowerDCMatrix(n);
long endMatrix = System.currentTimeMillis();
long timeMatrix = endMatrix-startMatrix;


//Ergebnisse auswerfen
System.out.println("Laufzeit recursive: " + timeRekursiv);
System.out.println("Laufzeit iterative: " + timeIterativ);
System.out.println("Laufzeit recursive: " + timeRekursiv);
System.out.println("Laufzeit power d&c: " + timeDC);
System.out.println("Laufzeit recursive: " + timeRekursiv);
System.out.println("Laufzeit matrixD&C: " + timeMatrix);
}
}
}