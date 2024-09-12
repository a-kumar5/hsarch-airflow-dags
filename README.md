## Hi there 👋

I'm **Ayush Kumar**, a passionate DevOps Engineer with 5 years of experience in **AWS**, **CI/CD pipelines**, and **Kubernetes automation**. I thrive on building efficient cloud infrastructures and automating complex processes to enhance system reliability.

```go
package main

import (
	"fmt"
)

type DevOpsEngineer struct {
	Name      string
	Experience int
	Skills     []string
}

func main() {
	ayush := DevOpsEngineer{
		Name:      "Ayush Kumar",
		Experience: 5,
		Skills:    []string{"AWS", "CI/CD", "Kubernetes", "Go", "Python"},
	}
	fmt.Printf("Hi there! I'm %s, a DevOps Engineer with %d years of experience.\n", ayush.Name, ayush.Experience)
}
