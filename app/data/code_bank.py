# File: app/data/code_bank.py
# -*- coding: utf-8 -*-
"""
[정리 완료] 코드형 문제 은행 (주관식 단답형)
- 모든 문제에 난이도(difficulty)와 카테고리(category) 필수 포함
- 난이도: 기초/중급/고급
- 카테고리: 코딩 (언어별로 language 필드 추가)
- 언어: Python/Java/C
"""

import textwrap

CODE_QUESTIONS = [
    # ========================================
    # [기초] Python 기본 (5문제)
    # ========================================
    {
        "q": "[코드] 다음 Python 클래스 상속 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            class Person:
                def __init__(self, name):
                    self.name = name
            
            class Student(Person):
                def __init__(self, name, id):
                    super().__init__(name)
                    self.id = id
            
            s = Student("Kim", 123)
            print(s.name, s.id)
        """),
        "answer": ["Kim 123"],
        "explain": "super().__init__(name)으로 부모 클래스 생성자를 호출합니다.",
        "difficulty": "기초",
        "category": "코딩",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python 리스트 pop 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [10, 20, 30]
            b = [a.pop(), a.pop()]
            print(b)
        """),
        "answer": ["[30, 20]"],
        "explain": "pop()은 마지막 요소를 꺼냅니다. 첫 pop()=30, 두 번째=20",
        "difficulty": "기초",
        "category": "코딩",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python 재귀 함수의 출력 결과는?\n\n" + textwrap.dedent("""
            def factorial(n):
                if n <= 1:
                    return 1
                else:
                    return n * factorial(n - 1)
            print(factorial(4))
        """),
        "answer": ["24"],
        "explain": "4 * 3 * 2 * 1 = 24입니다.",
        "difficulty": "기초",
        "category": "코딩",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python is 연산자 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = 10
            b = 10
            print(a is b)
        """),
        "answer": ["True"],
        "explain": "Python은 -5~256 정수를 캐싱하므로 같은 주소를 참조합니다.",
        "difficulty": "기초",
        "category": "코딩",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python global 키워드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            count = 0
            def inc():
                global count
                count += 1
            inc()
            inc()
            print(count)
        """),
        "answer": ["2"],
        "explain": "global 키워드로 전역 변수를 수정합니다.",
        "difficulty": "기초",
        "category": "코딩",
        "language": "Python"
    },
    
    # ========================================
    # [기초/중급] C언어 (11문제)
    # ========================================
    {
        "q": "[코드] 다음 C언어 Call by Reference 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            void swap(int *a, int *b) {
                int temp = *a;
                *a = *b;
                *b = temp;
            }
            int main() {
                int x = 10, y = 20;
                swap(&x, &y);
                printf("%d, %d", x, y);
                return 0;
            }
        """),
        "answer": ["20, 10", "20,10"],
        "explain": "포인터로 주소를 전달하여 원본 변수의 값을 교환합니다.",
        "difficulty": "기초",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 포인터 배열 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[3] = {10, 20, 30};
                int *p = arr;
                printf("%d", *(p + 2));
                return 0;
            }
        """),
        "answer": ["30"],
        "explain": "*(p + 2)는 p[2]와 같으며 배열의 3번째 요소입니다.",
        "difficulty": "기초",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 문자열 수정 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                char s[] = "ABC";
                s[1] = 'K';
                printf("%s", s);
                return 0;
            }
        """),
        "answer": ["AKC"],
        "explain": "배열 문자열은 수정 가능합니다. s[1]='B'를 'K'로 변경했습니다.",
        "difficulty": "기초",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 포인터 후위 연산 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[3] = {10, 20, 30};
                int *p = arr;
                printf("%d, ", *p++);
                printf("%d", *p);
                return 0;
            }
        """),
        "answer": ["10, 20", "10,20"],
        "explain": "*p++는 후위 연산으로 10을 출력 후 포인터가 증가합니다.",
        "difficulty": "중급",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 포인터 값 증가 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[3] = {10, 20, 30};
                int *p = arr;
                printf("%d, ", (*p)++);
                printf("%d", arr[0]);
                return 0;
            }
        """),
        "answer": ["10, 11", "10,11"],
        "explain": "(*p)++는 값을 1 증가시킵니다. 후위 연산으로 10 출력 후 증가합니다.",
        "difficulty": "중급",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 구조체 포인터 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            struct Person { int age; };
            void inc(struct Person *p) {
                p->age += 10;
            }
            int main() {
                struct Person p1 = {20};
                inc(&p1);
                printf("%d", p1.age);
                return 0;
            }
        """),
        "answer": ["30"],
        "explain": "포인터로 구조체의 멤버를 직접 수정합니다.",
        "difficulty": "중급",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 포인터 연산 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[5] = {10, 20, 30, 40, 50};
                int *p = arr;
                p++;
                int result = *p + arr[2];
                printf("%d", result);
                return 0;
            }
        """),
        "answer": ["50"],
        "explain": "p++로 p는 arr[1](20)을 가리킵니다. 20 + 30 = 50",
        "difficulty": "중급",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 static 변수 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int i, sum = 0;
                for (i = 0; i < 3; i++) {
                    static int num = 10;
                    sum += num;
                    num++;
                }
                printf("%d", sum);
                return 0;
            }
        """),
        "answer": ["33"],
        "explain": "static 변수는 값이 유지됩니다. 10 + 11 + 12 = 33",
        "difficulty": "고급",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 XOR 연산 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int a = 5, b = 3;
                a = a ^ b;
                b = a ^ b;
                a = a ^ b;
                printf("%d, %d", a, b);
                return 0;
            }
        """),
        "answer": ["3, 5", "3,5"],
        "explain": "XOR 연산을 이용한 swap 알고리즘입니다.",
        "difficulty": "고급",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 삼항 연산자 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int i = 0, sum = 0;
                while (i < 5) {
                    sum += (i % 2 == 0) ? i : -i;
                    i++;
                }
                printf("%d", sum);
                return 0;
            }
        """),
        "answer": ["2"],
        "explain": "짝수는 더하고 홀수는 뺍니다. 0 + (-1) + 2 + (-3) + 4 = 2",
        "difficulty": "중급",
        "category": "코딩",
        "language": "C"
    },
    {
        "q": "[코드] 다음 C언어 전위/후위 증감 연산 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int a = 5, b = 5;
                int result = ++a + b--;
                printf("%d, %d, %d", a, b, result);
                return 0;
            }
        """),
        "answer": ["6, 4, 11", "6,4,11"],
        "explain": "++a는 먼저 증가 후 사용(6), b--는 사용 후 감소(5→4). result = 6 + 5 = 11",
        "difficulty": "고급",
        "category": "코딩",
        "language": "C"
    },
    
    # ========================================
    # [기초/중급] Java (6문제)
    # ========================================
    {
        "q": "[코드] 다음 Java 오버라이딩 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            class Animal {
                void sound() { System.out.println("Animal sound"); }
            }
            class Dog extends Animal {
                @Override
                void sound() { System.out.println("Bark"); }
            }
            public class Main {
                public static void main(String[] args) {
                    Animal a = new Dog();
                    a.sound();
                }
            }
        """),
        "answer": ["Bark"],
        "explain": "실제 객체는 Dog이므로 오버라이딩된 메소드가 호출됩니다.",
        "difficulty": "기초",
        "category": "코딩",
        "language": "Java"
    },
    {
        "q": "[코드] 다음 Java == 연산자 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            public class Main {
                public static void main(String[] args) {
                    String s1 = new String("A");
                    String s2 = new String("A");
                    System.out.println(s1 == s2);
                }
            }
        """),
        "answer": ["false"],
        "explain": "==는 주소값을 비교합니다. new String()은 서로 다른 객체를 생성합니다.",
        "difficulty": "중급",
        "category": "코딩",
        "language": "Java"
    },
    {
        "q": "[코드] 다음 Java static 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            public class Main {
                static int a = 10;
                static void func() {
                    a = 30;
                }
                public static void main(String[] args) {
                    func();
                    System.out.println(a);
                }
            }
        """),
        "answer": ["30"],
        "explain": "static 변수는 모든 메소드에서 공유됩니다.",
        "difficulty": "기초",
        "category": "코딩",
        "language": "Java"
    },
    {
        "q": "[코드] 다음 Java 추상 클래스 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            abstract class Animal {
                abstract void sound();
            }
            class Dog extends Animal {
                void sound() { System.out.println("Bark"); }
            }
            public class Main {
                public static void main(String[] args) {
                    Animal a = new Dog();
                    a.sound();
                }
            }
        """),
        "answer": ["Bark"],
        "explain": "추상 메소드를 구현한 Dog의 sound()가 호출됩니다.",
        "difficulty": "중급",
        "category": "코딩",
        "language": "Java"
    },
    {
        "q": "[코드] 다음 Java super 키워드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            class Parent {
                void sound() { System.out.println("Parent"); }
            }
            class Child extends Parent {
                @Override
                void sound() { 
                    super.sound();
                    System.out.println("Child");
                }
            }
            public class Main {
                public static void main(String[] args) {
                    Parent p = new Child();
                    p.sound();
                }
            }
        """),
        "answer": ["Parent\nChild", "Parent Child"],
        "explain": "super.sound()로 부모 메소드를 먼저 호출합니다.",
        "difficulty": "중급",
        "category": "코딩",
        "language": "Java"
    },
    {
        "q": "[코드] 다음 Java static 변수/메소드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            public class Main {
                static int a = 10;
                static void add() {
                    a += 10;
                }
                public static void main(String[] args) {
                    Main.add();
                    System.out.println(Main.a);
                }
            }
        """),
        "answer": ["20"],
        "explain": "static 변수 a는 모든 객체가 공유합니다. add() 호출로 10에서 20으로 변경됩니다.",
        "difficulty": "중급",
        "category": "코딩",
        "language": "Java"
    },
    
    # ========================================
    # [중급] Python 고급 (4문제)
    # ========================================
    {
        "q": "[코드] 다음 Python 람다와 filter 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3, 4, 5, 6]
            b = list(filter(lambda x: x % 2 == 0, a))
            print(b)
        """),
        "answer": ["[2, 4, 6]"],
        "explain": "filter는 짝수만 걸러냅니다.",
        "difficulty": "중급",
        "category": "코딩",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python zip과 리스트 내포 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3]
            b = ['A', 'B', 'C']
            c = [n * s for n, s in zip(a, b)]
            print(c)
        """),
        "answer": ["['A', 'BB', 'CCC']"],
        "explain": "zip으로 짝지은 후 문자열을 n번 반복합니다.",
        "difficulty": "중급",
        "category": "코딩",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python 음수 슬라이싱 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [10, 20, 30, 40, 50]
            print(a[-3:-1])
        """),
        "answer": ["[30, 40]"],
        "explain": "음수 인덱스는 뒤에서부터 셉니다. -3(30)부터 -1(50) 전까지",
        "difficulty": "중급",
        "category": "코딩",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python 딕셔너리 get 메소드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            d = {'a': 1, 'b': 2}
            result = d.get('c', 0) + d.get('a', 0)
            print(result)
        """),
        "answer": ["1"],
        "explain": "get('c', 0)은 키가 없으면 기본값 0 반환. 0 + 1 = 1",
        "difficulty": "중급",
        "category": "코딩",
        "language": "Python"
    },
]
