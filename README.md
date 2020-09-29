This script will build the dependency tree for the a module and print out a list version of the tree. 
The first item on the list is the direct import into the project and then followed by the sub dependencies till the module been searched for is found. 
This script does require the use of `go mod`. 
Also note if the dependency graph is to large a recursion error with be throw.

**To Run**

The script is required to be ran from with in the go project folder but does not require to be in the root folder. 
If `go mod graph` works this script can work.

`python main.py <MOUDLE NAME>`

or create runnable script with `chmod +x main.py`

**Sample Print Out**
Below is the dependency tree where the searched for sub dependency is at the bottom of the list.
```
==================================================


github.com/operator-framework/operator-sdk@v0.15.2 <--Directly imported module
github.com/operator-framework/api@v0.0.0-20200120235816-80fd2f1a09c9
github.com/operator-framework/operator-lifecycle-manager@v0.0.0-20191115003340-16619cd27fa5
k8s.io/kubernetes@v1.16.0
github.com/docker/docker <--Searched for dependency


==================================================
```

After the tree has printed a list of packages and there version will be printed followed with usage number.
This aids with narrowing down root packages if the dependency tree is large.
```
Collecting package version usage count

github.com/Apicurio/apicurio-registry-operator
	v0.0.0-20200903111206-f9f14054bc16 : 6

github.com/operator-framework/operator-sdk
	v0.17.0 : 6
	v0.15.1 : 6
	v0.12.0 : 12
	v0.16.0 : 6
	v0.17.1 : 6
	v0.8.1-0.20190517223317-f7f644008098 : 6
	v0.0.0-20200428193249-b34ae44ff198 : 6
	v0.12.1-0.20191112211508-82fc57de5e5b : 18
	v0.19.0 : 6
	v0.14.0 : 6

github.com/helm/helm-2to3
	v0.5.1 : 26

helm.sh/helm/v3
	v3.1.0 : 26
	v3.1.2 : 56

```