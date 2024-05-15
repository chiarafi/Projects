import java.util.Random;

//////////////////////////
//Informatik II - SoSe 2020
//Task 1.2. a) b) c)
//////////////////////////

//////////////////////////
// Submission by: Chiara Fischer
// 
// 
//
//////////////////////////

public class InsertionSort {
	
	//////////////////////
	// Main function
	public static void main(String[] args) {
		// task 1.2.a)
		int[] list = {2,1,6,2,4,1,6};
		//printList(list);
		int[] newlist = insertionSort(list);
		printList(newlist);
		
		// task 1.2b)c)
		analyzeTimeComplexity(); 
	}

	//////////////////////
	// Helper function to print the elements of a list
	private static void printList(int[] list) {
		for(int i = 0; i < list.length; i++) {
			System.out.println(list[i]);
		}
	}

	//////////////////////
	// Task 1.2.a)
	// Implement the insertion sort algorithm based on
	// the lecture 1 (see slides 40 - 44)
   public static int[] insertionSort(int[] input_list) {
		
		for(int i = 1; i<input_list.length; i++) { // Schleife durchläuft vorliegende Folge ab dem 2.Element (da 1. Element bereits sortiert)
			int aktuell = input_list[i];          // Element an Stelle i unter Variable "aktuell" gespeichert
			int index = i-1;                      // Variable "index" speichert Stelle, die vor dem Element an Stelle i liegt
			while(index>=0 && aktuell<input_list[index]) { /* Schleife durchläuft Folge, bis Anfang erreicht wird oder 
			Element an Stelle i größer ist als das Element, das an der Stelle i-1 liegt */
				input_list[index+1] = input_list[index]; // an Stelle i wird das Element von der Position i-1 gesetzt, also um 1 nach hinten verschoben
				index--;
			}
			input_list[index+1] = aktuell; // Element der Stelle i wird am Position index+1 gespeichert 
		}
		return input_list;
	}

	//////////////////////
	// Task 1.2.b)
	// Create three lists of size n that create lists that are
	// average, best and worst case
	//
	// You can create random numbers by first creating a new
	// random number generator:
	//   Random rng = new Random();
	// Then retrieving a random number between 0 and K-1 using:
	//   int value = rng.nextInt(K);
	private static int[] generateAverageCase(int n) {
		 Random rng = new Random(); // neues Random Objekt
		 int[] randoms = new int[n];  // Array mit den random generierten Objekten von der Länge n, da dies den AverageCase darstellt
		 
		 int length = n;
		 int index=0;
		 while(length>0) {
		 int value=rng.nextInt(); //Speichert die Methodenrückgabe in der Variablen
		 randoms[index] = value;  // zufällig generiertes Objekt wird an der Stelle index im Array randoms gespeichert
		 index++;
		 length--;
		 }
		 return randoms;
	 
	}

	 private static int[] generateWorstCase(int n) {
			
		 int[] array= generateAverageCase(n);  // Array mit zufällig generierten Objekten wird erstellt
		 int[] sorted = insertionSort(array);  // Array wird sortiert; Name: sorted
		 
		 int indices = n-1;
		 int[] result = new int[n];
		 for(int i=0; i<n-1; i++) { // sorted wird umgekehrt auf neues Array übertragen, da der WorstCase beim Sortieralgorithmus eine umgekehrte Folge darstellt
			 result[indices] = sorted[i];
			 indices--;
			
		 }
		 return result;
		 
		 
		}

	private static int[] generateBestCase(int n) {
		int[] array = generateAverageCase(n);
		int[] sorted = insertionSort(array); // sortiertes Array erstellt, da dies den BestCase darstellt
		return sorted;
	}

	//////////////////////
	// Task 1.2.c)
	// Apply the function from 1.2.b for ascending n. Experiment
	// which nMin, nMax and step makes sense when iterating over n
	//   for(int n = nMin; n <= nMax; n += step)
	// and measure the time of the Insertion Sort function call.
	// Plot the results in an application of your choice
	//
	// You can get the current time using this java function:
	//    long start = System.currentTimeMillis();
	private static void analyzeTimeComplexity() {
		
		int nMax = 10000;
		int nMin = 1000;
		int step = 10000;
		
		for(int n=nMin; n<=nMax; n+=step) {
		// alle 3 Fälle werden erstellt und in Form von Arrays gespeichert
			int[] bestCase = generateBestCase(n);
			int[] averageCase = generateAverageCase(n);
			int[] worstCase = generateWorstCase(n);
		/* für die 3 Fälle wird zuerst der aktuelle Zeitpunkt gespeichert, 
		 * dann wird der Sortieralgorithmus auf den Fall angewendet und beim Abschließen des Algorithmus wird der Zeitpunkt erneut gespeichert
	     *  die Differenz der beiden Zeitpunkte stellt die Laufzeit des Algorithmus angewendet auf das Problem dar */
			long startBestCase = System.currentTimeMillis();
			insertionSort(bestCase);
			long endBestCase= System.currentTimeMillis();
			long timeBestCase = endBestCase-startBestCase;
			
			long startWorstCase = System.currentTimeMillis();
			insertionSort(worstCase);
			long endWorstCase= System.currentTimeMillis();
			long timeWorstCase = endWorstCase-startWorstCase;
			
			long startAverageCase = System.currentTimeMillis();
			insertionSort(averageCase);
			long endAverageCase= System.currentTimeMillis();
			long timeAverageCase = endAverageCase-startAverageCase;
			
			// Ausgabe der Ergebnisse 
			System.out.println("---");
			System.out.println("For n =" + n);
			System.out.println("BestCase: " + timeBestCase + " milliseconds");
			System.out.println("WorstCase: " + timeWorstCase + " milliseconds");
			System.out.println("AverageCase: " + timeAverageCase + " milliseconds");
			
			
		}
		
	}
}

