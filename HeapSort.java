import java.util.Random;

//////////////////////////
//Submission by:
//
//Chiara Fischer
//
//////////////////////////

public class HeapSort {
	public static void main(String[] args) {
		//////////////////////
		// Task 5.1.a)
		System.out.print("Test original Heap Sort");
		int[] list = new int[] {1, 5, 2, 9, 13, 4, 8};
		System.out.print("Before: "); 
		printList(list);
		sortOriginal(list);
		System.out.print("After:  "); 
		printList(list);
		
		
		
		//////////////////////
		// Task 5.1.b)
				System.out.print("Test Heap Sort Variant ");
				list = new int[] {1, 5, 2, 9, 13, 4, 8}; // reset list
				System.out.print("Before: "); 
				printList(list);
				sortVariant(list);
				System.out.print("After:  "); 
				printList(list);
				
				//////////////////////
				// Task 5.1.c)
				analzyeTimeComplexity();
	}
	
	//////////////////////
	// Task 5.1.a)
	// Implement the function sort that performs Heap Sort to sort the Heap A
	// in ascending order.


	public static void sortOriginal(int[] list) {
	build_Maxheap(list);  // Maxheap aufbauen aus der übergebenen Liste
	int end = list.length-1;
	//int size = list.length;
		while(end>=0) { // Indizes der nun absteigend sortierten Liste durchgehen (von hinten nach vorne)
			swap(list, end, 0); // für jedes i den Wert an der Stelle i mit dem Wert der Wurzel tauschen
		 // den neuen Wert der Wurzel mithilfe von Maxheap an die richtige Stelle im Baum setzen
			
			Maxheap(list,end,0);
			end--;
		
			} 
	
	}	
	
	
	//Hilfsfunktion Maxheap, um den Wert mit dem Index i solange in den Baum hinunterzureichen, bis er sich an der richtigen
	// Stelle befindet 
	
	public static void Maxheap(int[] list, int heapsize, int i) { // i ist ein übergebener Index
		int max = i; // max enthält Index
		// falls der Index des linken Kindes von list[i] sich noch im Baum befindet & der Wert des linken Kindes größer ist als
		// der Wert in list[i]
		if(getLeft(list,i)<heapsize && list[getLeft(list,i)] > list[max]) {
			max = getLeft(list,i); // max speichert nun den Index des linken Kindes
		}
		// falls der Index des rechten Kindes von list[i] sich noch im Baum befindet & der Wert des rechten Kindes größer ist als
	    // der Wert in list[max]
		if(getRight(list,i)<heapsize && list[getRight(list,i)] > list[max]) {
			max = getRight(list,i);
		}
		if(max!=i) { // falls max nicht mehr dem ursprünglichen i entspricht bedeutet das, dass das Kind an der Stelle list[max] größer
			// ist als der aktuelle Wert der Wurzel i
			swap(list, i, max); // tausche Werte list[i] und list[max]
			Maxheap(list,heapsize,max); // rekursives Weiterführen
		}
		
	}
	
	
	
	// Hulfsfunktion für das Tauschen von Elementen
	public static int[] swap(int[] list, int i, int j) {
		
		int x = list[i];
		int y = list[j];
		list[j] = x;
		list[i] = y;
		return list;
	}
	
	
	// Hilfsfunktion um Index des linken Kindes zu ermitteln
	public static int getLeft(int[] list, int i) {
	
		return 2*i+1;
	}
	
	// Hilfsfunktion um Index des rechten Kindes zu ermitteln
		public static int getRight(int[] list, int i) {
		
			return 2*i+2;
		}
		
	// Hilfsfunktion um Index des Elternknotens zu ermitteln
				public static int getParent(int[] list, int i) {
					return (i-1)/2;
	
		}

	
	// Hilfsfunktion Build_Maxheap
	// ruft für alle Nicht-Blätter die Maxheap Funktion auf
	
	public static int[] build_Maxheap(int[] list) {
	int size = list.length;
		for(int i=size/2-1; i>=0; i--) { // Start am letzten Elternknoten
			Maxheap(list,size,i);
		}
		
		return list;
	}
	
	
	//////////////////////
	// Task 5.1.b)
	// Implement the function sort that performs a Heap Sort variant as 
	// described in the exercise sheet to sort the Heap A in ascending order.
	public static void sortVariant(int[] list) {
		build_Maxheap(list);  // Maxheap aufbauen aus der übergebenen Liste
		int end = list.length-1; //  beginnt beim Index des letzten Elementes
		
			while(end>=0) { // Indizes des Maxheaps durchgehen (von hinten nach vorne), bis an der Wurzel angelangt
			swap(list, end, 0); // für jedes i den Wert an der Stelle i mit dem Wert der Wurzel tauschen

			
		    int x = list[0]; // Wert des nun in der Wurzel sitzenden Wertes merken
			FloatToLeaf(list,0, end); // Wert der Wurzel immer mit dem größeren Kindknotenwert tauschen, bis im Blatt angelangt
			
			BubbleUp(list,findPosition(list,x)); // falls die Maxheap-Eigenschaft zerstört wurde wird der soeben
			// durchgereichte Wert mithilfe dieser Funktion den Pfad wieder hochgereicht, bis die Maxheap Eigenschaft wieder
			// hergestellt wurde
           
			end--;
			
				} 
		
		}	
	
	// Hilfsfunktion, um die neue Position des Wertes x ausfindig zu machen
	public static int findPosition(int[] list, int x) {
		int position = 0;
	
		while(list[position]!=x) {
			position++;
		}
		return position;
	}
	
	
	// Funktion, um Wert in der Wurzel den Maxheap hinunter zu reichen und dabei immer mit dem größeren Kindknotenwert zu tauschen,
	// bis der Wert ein Blatt erreicht hat
	// Übergeben: Liste, i: der Index des durchzureichenden Wertes, end: Schranke, bis zu der der Wert hinuntergereicht werden darf
	public static int[] FloatToLeaf(int[] list, int i, int end) {
		
		
		if(i<=list.length/2-1) { // für alle Nicht-Blätter aufrufen
		// Wert der Wurzel wird immer mit dem größeren Kind vertauscht
			
			// falls betrachteter Knoten i 2 Kinder besitzt
			// und der Wert des linken Kindknotens größer ist als der des rechten 
			// und falls der linke Kindknoten unterhalb der oberen Grenze end liegt
			if(getLeft(list, i) < end && list[getLeft(list, i)]>list[getRight(list, i)] ) {
			   swap(list, i, getLeft(list, i));
	           int x = getLeft(list, i);
			   FloatToLeaf(list, x, end);
				
			 // falls betrachteter Knoten i 2 Kinder besitzt
		     // und der Wert des rechten Kindknotens größer ist als der des linken
			 // und falls der rechte Kindknoten unterhalb der oberen Grenze end liegt
		   }else  if(getRight(list, i) < end && list[getRight(list, i)]>list[getLeft(list, i)] ) {
			   swap(list, i, getRight(list, i));
			   int x = getRight(list, i);
			   FloatToLeaf(list, x, end);
				
		    // falls betrachteter Knoten i 1 Kind besitzt (dies ist dann der Linke)
			// und dieser Kindknoten unterhalb der oberen Grenze end liegt
		} else if(getLeft(list, i) < end && list[getRight(list, i)]>list[getLeft(list, i)] ) {
			 swap(list, i, getLeft(list, i));
	   int x = getLeft(list, i);
	   FloatToLeaf(list, x, end);
 		}
		}
		return list;
	}
	
	
	// Funktion, um Knoten rekusriv den Pfad hinaufzureichen, bis die Maxheap Eigenschaft besteht
	// Übergeben: Liste, stelle: Index des zu betrachtenden Knotens
	public static int[] BubbleUp(int[] list, int stelle) {
	
		// falls der Index >=1 (d.h. Knoten ist nicht die Wurzel) und der Wert des Elternknotens kleiner
		// ist als der Wert des betrachtenden Knotens (d.h. Maxheap Eigenschaft besteht hier nicht)
		 if(stelle>=1 && list[getParent(list,stelle)]<list[stelle] ) {
			swap(list, stelle, getParent(list,stelle)); // Tausche Elternknoten mit Knoten 
			BubbleUp(list,getParent(list,stelle)); // führe dies rekursiv fort für den Knoten, der sich nun an der Stelle befindet
			// an der sich zuvor der Elternknoten befand
		}
return list;
}
	
	//////////////////////
	// Task 5.1.c)
	// Analyze the time complexity of the original heap sort implementation and
	// it's variant for heaps of different lengths (make sure to include very
	// large heaps)
	
	private static int[] generateList(int n) {
		int[] list = new int[n];
		
		Random r = new Random();
		for(int i = 0; i < n; i++) {
			list[i] = r.nextInt(10000);
		}
		
		return list;
	}
	
	
	public static void analzyeTimeComplexity() {
		int nMax = 50000;
		int nMin = 10;
		int step = 5000;

		for(int n=nMin; n<=nMax; n+=step) {
        int[] list = generateList(n);

		// Laufzeit a)
		long start = System.currentTimeMillis();
		sortOriginal(list);
		long end= System.currentTimeMillis();
		long timeFirst = end-start;

		

		// Laufzeit b)
		long start2 = System.currentTimeMillis();
		sortVariant(list);
		long end2 = System.currentTimeMillis();
		long timeSecond = end2-start2;


		//Ergebnisse auswerfen
		System.out.println("Laufzeit a): " + timeFirst);
		System.out.println("Laufzeit b): " + timeSecond);
		}


// Mir fällt auf: der sortVariant Algorithmus ist für große Eingabegrößen besser geeignet, läuft also schneller. Für kleinere Eingabegrößen eignet sich der 
// sortOriginal Algorithmus besser (bei den von uns verwendeten Schritten wechselt der schneller laufende Algorithmus
// vom Algorithmus sortOriginal auf den sortVariant ab einer Eingabegröße von 35000)


}

	// helper function to print a list
	public static void printList(int[] list) {
		String msg = "[";
		for(int i = 0; i < list.length; i++) {
			msg += list[i];
			if(i+1 < list.length) msg += ", ";
		}
		msg += "]";
		System.out.println(msg);
	}
}
