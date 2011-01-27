Independent Study in Genetic Algorithms

The following is my proposal for studying genetic algorithms and the MOCK algorithm.

What is Clustering?
Clustering or cluster analysis is the practice of assigning data elements in a data set to subsets which are called clusters. The data elements in the each cluster are considered similar based on one or more objective function. This technique is used in many fields such as machine learning, data mining and image processing to name a few [MATAKE01] [SHIRAKAWA01]. Clustering is a not a well defined concept  and is not very easily realized due to the fact that for a sizable number of data sets there is no way to partition unambiguously [HANDL01].  

Clustering Techniques
According to [HANDL01], one way to classify clustering algorithms is based on the clustering criterion of  compactness and connectedness. Compactness means that the variation between data elements in the same cluster is small which is usually determined by Euclidean distance. Connectedness means that the data elements should share the same cluster. This means the main tasks in clustering are finding the number of clusters, typically called k, in a data set and figuring out how to partition the data elements into those k clusters. The most widely used data clustering techniques are k-means and agglutination method.  K-means is best used for partitioning the data set into k-clusters while the agglutination method is best for determining what the k clusters are.  [MATAKE01] Both k-means and agglutination clustering methods use one objective function.  The k-means objective is concerned with the compactness of clusters while agglutination with connectedness. 

Clustering can be considered a multiobjective problem (MOP). MOPs are problems where the  quality of a solution is determined by its performance in several, possibly competing, objectives. The use single-objective algorithms such as k-means is usually done to make the problem more tractable [EIBEN01]. [HANDL01] proposed a multiobjective evolutionary algorithm (MOEA) that used the previously mentioned objectives of compactness and connectedness called Multiobjective clustering with automatic k-determination (MOCK).  The MOCK algorithm optimizes these two complimentary objectives (compactness and connectedness). The MOCK algorithm is based on the Pareto envelope selection algorithm version 2 (PESA2) which is a multiobjective evolutionary algorithm that uses 'niching' in objective space to spread the population over the Pareto front. The Pareto front is the set of all non-dominated solutions which are solutions whose quality with respect to the object functions cannot be improved without adversely affecting the other solutions in the set [EIBEN01] [DEBK]. PESA2 also uses the concept of elitism to reduce the need for parameter settings necessary for evolutionary algorithms so that the loss of non-dominated solutions is discouraged and convergence towards the Pareto front is encouraged.

My proposal
As a newcomer to evolutionary computation, my goal is to learn about this field through the understanding of all the pieces that compose the MOCK algorithm and deliver my own implementation of that algorithm and test it on one or more UC Irvine machine learning data set(s) [UCIMACH01]. I will use Goldberg's book Genetic Algorithms in Search Optimization & Machine Learning [GOLDBERGD] and Deb's book Multi-Objective Optmization using Evolutionary Algorithms as guides to learning the concept involved in MOCK. 

     
[Week 1] Goldberg: Ch 1-3, implement first genetic algorithm
[Week 2] Goldberg: Ch 4-5, learn about  GA applications and advanced operators and techniques in genetic search
[Week 3] Deb: Ch 1-3, Prologue, Multi-Objective Optimization concepts (Pareto front, single Objective vs Multi-Objective Optmization, Dominance and Pareto Optimality), Classical Optimization
[Week 4] Deb: Ch 4-5, EAs and Non-elitist MOEA
[Week 5] Deb: Ch 6,8, Elitist MOEA and MOEA Issues
[Week 6 -10] Study MOCK [MATAKE01] and implement 

Bibliography
MATAKE01: Matake, N. Hiroyasu, T. Miki, M. Senda, T., Multiobjective Clustering with Automatic k-determinationfor Large-scale Data, 2007
SHIRAKAWA01: Shirakawa, S. Nagao, T., Evolutionary Image SegmentationBased on Multiobjective Clustering, 2007?
HANDL01: Handl, Julia. Knowles, Joshua., Multiobjective Clustering with automatic determination of the number of clusters, 2004
EIBEN01: Eiben, A.E. Smith, J.E., Introduction to Evolutionary Computing, 2003
DEBK: Deb K., Multi-Objective Optimization using Evolutionary Algorithms, 2009
UCIMACH01: , http://archive.ics.uci.edu/ml/, , http://archive.ics.uci.edu/ml/
