
public class MatrixMult2 {
	
	    public static void main (String[] args)
	    {
	      

	        int[][] matrix1S = {{2,1,2,1,2,0},{3,2,3,1,2,0}, {4,3,4,1,2,0},{1,1,1,1,1,0}, {1,1,1,1,1,0}, {0,0,0,0,0,0}};
	        int[][] matrix2S = {{2,2,2,1,2,0},{2,2,2,1,2,0}, {1,1,1,1,1,0}, {1,1,1,1,1,0}, {2,2,2,1,2,0}, {0,0,0,0,0,0}}; 
	 
	       printMatrix((strassen(matrix1S, matrix2S))); 
	       
	       System.out.println(sucheZweierpotenz(matrix1S.length));
	     
	    }

	    //////////////////////
		// Helper function to print the elements of a matrix
		private static void printMatrix(int[][] matrix) {
			for(int i = 0; i < matrix.length; i++) {
	            for(int j = 0; j < matrix[i].length; j++) {
				    System.out.print(matrix[i][j]);
				    System.out.print(" ");
	            }
	            System.out.print("\n");
			}
			System.out.print("\n");
		}

	    /////////////////////
	    // Matrix multiplication (Strassen) for n x n matrices with n power of 2
	    // Task 4.2a
	    public static int[][] strassen(int[][] m1, int[][] m2) {

	        
	        // Teilmatrizen definieren
	        int[][] a = new int[m1.length/2][m1.length/2];
	        int[][] b = new int[m1.length/2][m1.length/2];
	        int[][] c = new int[m1.length/2][m1.length/2];
	        int[][] d = new int[m1.length/2][m1.length/2];
	        
	        int[][] e = new int[m1.length/2][m1.length/2];
	        int[][] f = new int[m1.length/2][m1.length/2];
	        int[][] g = new int[m1.length/2][m1.length/2];
	        int[][] h = new int[m1.length/2][m1.length/2];
	        
	        // a
	        for(int i=0; i<m1.length/2; i++) {
	        	for(int j=0; j<m1.length/2; j++) {
	        		a[i][j] = m1[i][j];
	        	}
	        }
	        // e
	        for(int i=0; i<m1.length/2; i++) {
	        	for(int j=0; j<m1.length/2; j++) {
	        		e[i][j] = m2[i][j];
	        	}
	        }
	     
	        //b
	        for(int i=0; i<m1.length/2; i++) {
	        	int index=m1.length/2;
	        	for(int j=0; j<m1.length/2; j++) {
	        		
	        		b[i][j] = m1[i][index];
	        		index++;
	        	}
	        
	        }
	        
	        //f
	        for(int i=0; i<m1.length/2; i++) {
	        	int index=m1.length/2;
	        	for(int j=0; j<m1.length/2; j++) {
	        		
	        		f[i][j] = m2[i][index];
	        		index++;
	        	}
	        
	        }
	        
	        //c
	        int index5 = m1.length/2;
	        for(int i=0; i<m1.length/2; i++) {
	        	
	        	for(int j=0; j<m1.length/2; j++) {
	        		c[i][j] = m1[index5][j];
	        		
	        	}
	        	index5++;
	        }
	        
	        //g
	        int index2 =m1.length/2;
	        for(int i=0; i<m1.length/2; i++) {
	        	
	        	for(int j=0; j<m1.length/2; j++) {
	        		g[i][j] = m2[index2][j];
	        		
	        	}
	        	index2++;
	        }
	        
	        //d
	        int index3 =m1.length/2;
	        for(int i=0; i<m1.length/2; i++) {
	        	int index1=m1.length/2;
	        	for(int j=0; j<m1.length/2; j++) {
	        		
	        		d[i][j] = m1[index3][index1];
	        		index1++;
	        	}
	        	index3++;
	        }
	        
	        //h
	        int index4 =m1.length/2;
	        for(int i=0; i<m1.length/2; i++) {
	        	int index1=m1.length/2;
	        	for(int j=0; j<m1.length/2; j++) {
	        		
	        		h[i][j] = m2[index4][index1];
	        		index1++;
	        	}
	        	index4++;
	        }
	       
	     // Teillösungen aufstellen
	        int[][] p1 = new int[m1.length/2][m1.length/2];
	        int [][] p1result = multiply(a, (subtract(f,h)));
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        		p1[i][k] = p1result[i][k];
	        	}
	        }
	        
	        
	        int[][] p2 = new int[m1.length/2][m1.length/2];
	        int [][] p2result = multiply((add(a,b)), h);
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        		p2[i][k] = p2result[i][k];
	        	}
	        }
	        
	        
	        int[][] p3 = new int[m1.length/2][m1.length/2];
	        int [][] p3result = multiply((add(c,d)), e);
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        		p3[i][k] = p3result[i][k];
	        	}
	        }
	        
	        
	        int[][] p4 = new int[m1.length/2][m1.length/2];
	        int [][] p4result = multiply(d,(subtract(g,e)));
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        		p4[i][k] = p4result[i][k];
	        	}
	        }
	        
	        
	        int[][] p5 = new int[m1.length/2][m1.length/2];
	        int [][] p5result = multiply((add(a,d)), (add(e,h)));
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        		p5[i][k] = p5result[i][k];
	        	}
	        }
	        
	        
	        int[][] p6 = new int[m1.length/2][m1.length/2];
	        int [][] p6result = multiply(subtract(b,d), add(g,h));
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        		p6[i][k] = p6result[i][k];
	        	}
	        }
	        
	        
	        int[][] p7 = new int[m1.length/2][m1.length/2];
	        int [][] p7result = multiply(subtract(a,c), add(e,f));
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        		p7[i][k] = p7result[i][k];
	        	}
	        }
	        
	      //kombinieren
	        
	        int[][] result = new int[m1.length][m1.length];
	        
	        int[][] r = new int[p1.length][p1.length];
	        int[][] rResult = subtract(add(add(p5, p4), p6), p2);
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        		r[i][k] = rResult[i][k];
	        	}
	        }
	        
	        int[][] s = new int[p1.length][p1.length];
	        int[][] sResult = add(p1,p2);
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        		s[i][k] = sResult[i][k];
	        	}
	        }
	        
	        int[][] t = new int[p1.length][p1.length];
	        int[][] tResult = add(p3,p4);
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        	t[i][k] = tResult[i][k];
	        	}
	        }
	        
	        int[][] u = new int[p1.length][p1.length];
	        int[][] uResult = subtract(subtract(add(p5,p1), p3), p7);
	        for(int i=0; i<p1.length; i++) {
	        	for(int k=0; k<p1.length; k++) {
	        	u[i][k] = uResult[i][k];
	        	}
	        }
	      
	      
	        for(int i=0; i<m1.length/2; i++) {
	        	for(int j=0; j<m1.length/2; j++) {
	        		result[i][j] = r[i][j];
	        	}
	        }
	        
	        int index0 = m1.length/2;
	        for(int i=0; i<m1.length/2; i++) {
	        	
	        	for(int j=0; j<m1.length/2; j++) {
	        		result[index0][j] = t[i][j];
	        	}
	        	index0++;
	        }
	        
	        for(int i=0; i<m1.length/2; i++) {
	        	int index = m1.length/2;
	        	for(int j=0; j<m1.length/2; j++) {
	        		
	        		result[i][index] = s[i][j];
	        		index++;
	        	}
	        	
	        }
	        
	        
	        for(int i=0; i<m1.length/2; i++) {
	        	int index6 = m1.length/2;
	        	for(int j=0; j<m1.length/2; j++) {
	        		int index = m1.length/2;
	        		result[index6][index] = u[i][j];
	        		index++;
	        	}
	        	index6++;
	        }
	        
	        return result;
	    }
	    
	    
	    
	    
	    
	    
	    
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
	    
	    
	    
	    
	    
	    
	    
	    public static int[][] subtract(int[][] m1, int[][] m2) {
	    	int[][] result = new int[m1.length][m1.length];
	    	for(int i=0; i<m1.length; i++) {
	    		for(int j=0; j<m1.length; j++) {
	    			result[i][j] = m1[i][j] - m2[i][j];
	    		}
	    	}
	    	return result;
	    }
	    
	    public static int[][] add(int[][] m1, int[][] m2) {
	    	int[][] result = new int[m1.length][m1.length];
	    	for(int i=0; i<m1.length; i++) {
	    		for(int j=0; j<m1.length; j++) {
	    			result[i][j] = m1[i][j] + m2[i][j];
	    		}
	    	}
	    	return result;
	    }
	    
	   
	    
	    
	    public static int[][] strassenGeneral(int[][] m1, int[][] m2) {
	        
	         if(m1.length%2!=0) {
	         	int[][] newM1 = new int[m1.length+1][m1.length+1];
	         	for(int i=0; i<m1.length;i++) {
	         		for(int j=0; j<m1.length;j++) {
	         			newM1[i][j] = m1[i][j];
	         		}
	         	}
	         	for(int i=0; i<m1.length+1;i++) {
	         		for(int j=m1.length; j<m1.length+1;j++) {
	         			newM1[i][j] = 0;
	         		}
	         	}
	         	
	         	for(int i=m1.length; i<m1.length+1;i++) {
	         		for(int j=0; j<m1.length+1;j++) {
	         			newM1[i][j] = 0;
	         		}
	         	}
	         	
	         	int[][] newM2 = new int[m1.length+1][m1.length+1];
	         	for(int i=0; i<m1.length;i++) {
	         		for(int j=0; j<m1.length;j++) {
	         			newM2[i][j] = m2[i][j];
	         		}
	         	}
	         	for(int i=0; i<m1.length+1;i++) {
	         		for(int j=m1.length; j<m1.length+1;j++) {
	         			newM2[i][j] = 0;
	         		}
	         	}
	         
	         	for(int i=m1.length; i<m1.length+1;i++) {
	         		for(int j=0; j<m1.length+1;j++) {
	         			newM2[i][j] = 0;
	         		}
	         	}
	         	
	         	
	         	int[][] result = strassen(newM1,newM2);
	         	int[][] endresult = new int[result.length-1][result.length-1];
	         	
	         	for(int i=0; i<endresult.length;i++) {
	         		for(int j=0; j<endresult.length;j++) {
	         			endresult[i][j] = result[i][j];
	         		}
	         	}
	         	
	         	return endresult;
	       
	         
	         	
	         }
	         else {
	         	return (strassen(m1,m2));
	         }
	     }
	    
	    public static int sucheZweierpotenz(int a) {
			int b = a;
			while(zweierpotenz(b)==0) {
				b++;
			}
			return b;
		}
	    
	    public static int zweierpotenz(int a) {
	    	if(a==1) {return 1;}
	    	if(a%2==0) {return zweierpotenz(a/2);}
	    	return 0;
	    }
	    
	    
}
