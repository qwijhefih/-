# File: app/data/code_bank.py
# -*- coding: utf-8 -*-
"""
[정리 완료] 코드형 문제 은행 (주관식 단답형)
- 중복 제거: 동일 문제 3개 제거
- 난이도 분류: 기초/중급/고급
- 언어별 분류: Python/Java/C
- 2024년 최신 출제 경향 반영
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
        "answer": "Kim 123",
        "explain": "super().__init__(name)으로 부모 클래스 생성자를 호출합니다.",
        "difficulty": "기초",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python 리스트 pop 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [10, 20, 30]
            b = [a.pop(), a.pop()]
            print(b)
        """),
        "answer": "[30, 20]",
        "explain": "pop()은 마지막 요소를 꺼냅니다. 첫 pop()=30, 두 번째=20",
        "difficulty": "기초",
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
        "answer": "24",
        "explain": "4 * 3 * 2 * 1 = 24입니다.",
        "difficulty": "기초",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python is 연산자 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = 10
            b = 10
            print(a is b)
        """),
        "answer": "True",
        "explain": "Python은 -5~256 정수를 캐싱하므로 같은 주소를 참조합니다.",
        "difficulty": "기초",
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
        "answer": "2",
        "explain": "global 키워드로 전역 변수를 수정합니다.",
        "difficulty": "기초",
        "language": "Python"
    },
    # ========================================
    # [기초/중급] C언어 (10문제)
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
        "answer": "20, 10",
        "explain": "포인터로 주소를 전달하여 원본 변수의 값을 교환합니다.",
        "difficulty": "기초",
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
        "answer": "30",
        "explain": "*(p + 2)는 p[2]와 같으며 배열의 3번째 요소입니다.",
        "difficulty": "기초",
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
        "answer": "AKC",
        "explain": "배열 문자열은 수정 가능합니다. s[1]='B'를 'K'로 변경했습니다.",
        "difficulty": "기초",
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
        "answer": "30",
        "explain": "포인터로 구조체의 멤버를 직접 수정합니다.",
        "difficulty": "중급",
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
        "answer": "50",
        "explain": "p++로 p는 arr[1](20)을 가리킵니다. 20 + 30 = 50",
        "difficulty": "중급",
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
        "answer": "33",
        "explain": "static 변수는 값이 유지됩니다. 10 + 11 + 12 = 33",
        "difficulty": "고급",
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
        "answer": "3, 5",
        "explain": "XOR 연산을 이용한 swap 알고리즘입니다.",
        "difficulty": "고급",
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
        "answer": "2",
        "explain": "짝수는 더하고 홀수는 뺍니다. 0 + (-1) + 2 + (-3) + 4 = 2",
        "difficulty": "중급",
        "language": "C"
    },
    # ========================================
    # [기초/중급] Java (5문제)
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
        "answer": "Bark",
        "explain": "실제 객체는 Dog이므로 오버라이딩된 메소드가 호출됩니다.",
        "difficulty": "기초",
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
        "answer": "false",
        "explain": "==는 주소값을 비교합니다. new String()은 서로 다른 객체를 생성합니다.",
        "difficulty": "중급",
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
        "answer": "30",
        "explain": "static 변수는 모든 메소드에서 공유됩니다.",
        "difficulty": "기초",
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
        "answer": "Bark",
        "explain": "추상 메소드를 구현한 Dog의 sound()가 호출됩니다.",
        "difficulty": "중급",
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
        "language": "Java"
    },
    # ========================================
    # [중급] Python 고급 (5문제)
    # ========================================
    {
        "q": "[코드] 다음 Python 람다와 filter 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3, 4, 5, 6]
            b = list(filter(lambda x: x % 2 == 0, a))
            print(b)
        """),
        "answer": "[2, 4, 6]",
        "explain": "filter는 짝수만 걸러냅니다.",
        "difficulty": "중급",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python zip과 리스트 내포 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3]
            b = ['A', 'B', 'C']
            c = [n * s for n, s in zip(a, b)]
            print(c)
        """),
        "answer": "['A', 'BB', 'CCC']",
        "explain": "zip으로 짝지은 후 문자열을 n번 반복합니다.",
        "difficulty": "중급",
        "language": "Python"
    },
    {
        "q": "[코드] 다음 Python 음수 슬라이싱 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [10, 20, 30, 40, 50]
            print(a[-3:-1])
        """),
        "answer": "[30, 40]",
        "explain": "음수 인덱스는 뒤에서부터 셉니다. -3(30)부터 -1(50) 전까지",
        "difficulty": "중급",
        "language": "Python"
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
        "answer": "30",
        "explain": "포인터 p는 배열 arr의 시작 주소를 가리킵니다. *(p + 2)는 p[2]와 같으며, 배열의 3번째 요소인 30을 의미합니다."
    },
    {
        "q": "[코드] 다음 Java 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            public class Main {
                public static void main(String[] args) {
                    String s1 = new String("A");
                    String s2 = new String("A");
                    System.out.println(s1 == s2);
                }
            }
        """),
        "answer": "false",
        "explain": "'==' 연산자는 두 객체의 주소값을 비교합니다. new String()으로 생성된 s1과 s2는 내용물('A')은 같지만 서로 다른 주소를 가집니다. (내용 비교는 s1.equals(s2)를 써야 함)"
    },
    {
        "q": "[코드] 다음 Python 재귀 함수 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            def factorial(n):
                if n <= 1:
                    return 1
                else:
                    return n * factorial(n - 1)
            print(factorial(4))
        """),
        "answer": "24",
        "explain": "4 * f(3) -> 4 * (3 * f(2)) -> 4 * (3 * (2 * f(1))) -> 4 * 3 * 2 * 1 = 24입니다."
    },
    {
        "q": "[코드] 다음 C언어 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                char s[] = "ABC";
                s[1] = 'K';
                printf("%s", s);
                return 0;
            }
        """),
        "answer": "AKC",
        "explain": "배열 s[]는 수정 가능한 문자열입니다. s[1] (두 번째 문자 'B')를 'K'로 변경했습니다."
    },
    {
        "q": "[코드] 다음 Python 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = 10
            b = 10
            print(a is b)
        """),
        "answer": "True",
        "explain": "파이썬은 -5부터 256까지의 정수를 미리 캐싱(저장)해둡니다. a와 b는 같은 메모리 주소를 참조하므로 'is' 비교(주소 비교)가 True입니다."
    },
    {
        "q": "[코드] 다음 Java 코드의 출력 결과는?\n\n" + textwrap.dedent("""
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
        "answer": "30",
        "explain": "a가 static(정적) 변수이므로 func() 메소드에서 변경한 값이 main 메소드에 영향을 미칩니다."
    },
    # --- 심화 (Comprehension, Lambda, static, Pointer) (Set 8) ---
    {
        "q": "[코드] 다음 Python '람다(Lambda)'와 'filter' 함수 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3, 4, 5, 6]
            b = list(filter(lambda x: x % 2 == 0, a))
            print(b)
        """),
        "answer": ["[2, 4, 6]"],
        "explain": "filter 함수는 리스트 a의 요소 중 lambda 함수(x % 2 == 0, 즉 짝수)를 True로 만드는 값만 걸러냅니다."
    },
    {
        "q": "[코드] 다음 Python 'zip'과 '리스트 내포' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3]
            b = ['A', 'B', 'C']
            c = [n * s for n, s in zip(a, b)]
            print(c)
        """),
        "answer": ["['A', 'BB', 'CCC']"],
        "explain": "zip(a, b)는 (1, 'A'), (2, 'B'), (3, 'C')를 짝지어줍니다. n * s는 문자열 반복을 의미합니다. (1*'A', 2*'B', 3*'C')"
    },
    {
        "q": "[코드] 다음 C언어 '포인터 연산' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[3] = {10, 20, 30};
                int *p = arr;
                printf("%d, ", *p++); // 후위
                printf("%d", *p);
                return 0;
            }
        """),
        "answer": ["10, 20", "10,20"],
        "explain": "*p++는 후위 연산입니다. *p (10)을 먼저 출력하고, 그 후에 포인터 p가 1 증가하여 arr[1] (20)을 가리킵니다."
    },
    {
        "q": "[코드] 다음 C언어 '포인터 연산' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[3] = {10, 20, 30};
                int *p = arr;
                printf("%d, ", (*p)++); // 괄호
                printf("%d", arr[0]);
                return 0;
            }
        """),
        "answer": ["10, 11", "10,11"],
        "explain": "(*p)++는 p가 가리키는 *값*을 1 증가시킵니다. printf는 후위 연산이므로 현재 값 10을 먼저 출력하고, 그 후 arr[0]의 값이 11로 바뀝니다."
    },
    {
        "q": "[코드] 다음 C언어 '구조체 포인터' 함수 코드의 출력 결과는?\n\n" + textwrap.dedent("""
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
        "explain": "inc 함수에 p1의 주소(&p1)를 넘겼습니다. 포인터 p가 p1을 가리키므로, p->age는 p1.age를 의미합니다. (20 + 10 = 30)"
    },
    {
        "q": "[코드] 다음 Java 'static(정적) 변수/메소드' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
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
        "explain": "static 변수 a는 모든 객체가 공유합니다. static 메소드 add()가 호출되어 Main.a의 값이 10에서 20으로 변경되었습니다."
    },
    {
        "q": "[코드] 다음 Java '추상 클래스(abstract)' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            abstract class Animal {
                abstract void sound(); // 추상 메소드
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
        "explain": "추상 클래스 Animal을 상속받은 Dog 클래스가 추상 메소드 sound()를 'Bark'로 구현(오버라이딩)했습니다."
    },
    {
        "q": "[코드] 다음 Java 'super' 키워드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            class Parent {
                void sound() { System.out.println("Parent"); }
            }
            class Child extends Parent {
                @Override
                void sound() { 
                    super.sound(); // 1. 부모 sound() 호출
                    System.out.println("Child"); // 2. 자기 sound() 실행
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
        "explain": "자식(Child)의 sound()가 호출되었지만, 내부에서 super.sound()를 통해 부모(Parent)의 'Parent'가 먼저 출력되고, 그 다음 'Child'가 출력됩니다."
    },
    {
        "q": "[코드] 다음 Python 'global' 키워드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            count = 0
            def inc():
                global count
                count += 1
            inc()
            inc()
            print(count)
        """),
        "answer": ["2"],
        "explain": "'global count' 키워드로 인해, inc() 함수가 호출될 때마다 전역 변수 count의 값이 1씩 증가합니다."
    },
    {
        "q": "[코드] 다음 Python '음수 슬라이싱' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [10, 20, 30, 40, 50]
            print(a[-3:-1])
        """),
        "answer": ["[30, 40]"],
        "explain": "음수 인덱스는 뒤에서부터 셉니다. (-1은 50, -2는 40, -3은 30). a[-3] (30)부터 a[-1] (50) *전*까지, 즉 [30, 40]이 출력됩니다."
    },
    # --- 심화 (Comprehension, Lambda, static, Pointer) (Set 8) ---
    {
        "q": "[코드] 다음 Python '람다(Lambda)'와 'filter' 함수 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3, 4, 5, 6]
            b = list(filter(lambda x: x % 2 == 0, a))
            print(b)
        """),
        "answer": ["[2, 4, 6]"],
        "explain": "filter 함수는 리스트 a의 요소 중 lambda 함수(x % 2 == 0, 즉 짝수)를 True로 만드는 값만 걸러냅니다."
    },
    {
        "q": "[코드] 다음 Python 'zip'과 '리스트 내포' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3]
            b = ['A', 'B', 'C']
            c = [n * s for n, s in zip(a, b)]
            print(c)
        """),
        "answer": ["['A', 'BB', 'CCC']"],
        "explain": "zip(a, b)는 (1, 'A'), (2, 'B'), (3, 'C')를 짝지어줍니다. n * s는 문자열 반복을 의미합니다. (1*'A', 2*'B', 3*'C')"
    },
    {
        "q": "[코드] 다음 C언어 '포인터 연산' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[3] = {10, 20, 30};
                int *p = arr;
                printf("%d, ", *p++); // 후위
                printf("%d", *p);
                return 0;
            }
        """),
        "answer": ["10, 20", "10,20"],
        "explain": "*p++는 후위 연산입니다. *p (10)을 먼저 출력하고, 그 후에 포인터 p가 1 증가하여 arr[1] (20)을 가리킵니다."
    },
    {
        "q": "[코드] 다음 C언어 '포인터 연산' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[3] = {10, 20, 30};
                int *p = arr;
                printf("%d, ", (*p)++); // 괄호
                printf("%d", arr[0]);
                return 0;
            }
        """),
        "answer": ["10, 11", "10,11"],
        "explain": "(*p)++는 p가 가리키는 *값*을 1 증가시킵니다. printf는 후위 연산이므로 현재 값 10을 먼저 출력하고, 그 후 arr[0]의 값이 11로 바뀝니다."
    },
    {
        "q": "[코드] 다음 C언어 '구조체 포인터' 함수 코드의 출력 결과는?\n\n" + textwrap.dedent("""
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
        "explain": "inc 함수에 p1의 주소(&p1)를 넘겼습니다. 포인터 p가 p1을 가리키므로, p->age는 p1.age를 의미합니다. (20 + 10 = 30)"
    },
    {
        "q": "[코드] 다음 Java 'static(정적) 변수/메소드' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
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
        "explain": "static 변수 a는 모든 객체가 공유합니다. static 메소드 add()가 호출되어 Main.a의 값이 10에서 20으로 변경되었습니다."
    },
    {
        "q": "[코드] 다음 Java '추상 클래스(abstract)' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            abstract class Animal {
                abstract void sound(); // 추상 메소드
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
        "explain": "추상 클래스 Animal을 상속받은 Dog 클래스가 추상 메소드 sound()를 'Bark'로 구현(오버라이딩)했습니다."
    },
    {
        "q": "[코드] 다음 Java 'super' 키워드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            class Parent {
                void sound() { System.out.println("Parent"); }
            }
            class Child extends Parent {
                @Override
                void sound() { 
                    super.sound(); // 1. 부모 sound() 호출
                    System.out.println("Child"); // 2. 자기 sound() 실행
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
        "explain": "자식(Child)의 sound()가 호출되었지만, 내부에서 super.sound()를 통해 부모(Parent)의 'Parent'가 먼저 출력되고, 그 다음 'Child'가 출력됩니다."
    },
    {
        "q": "[코드] 다음 Python 'global' 키워드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            count = 0
            def inc():
                global count
                count += 1
            inc()
            inc()
            print(count)
        """),
        "answer": ["2"],
        "explain": "'global count' 키워드로 인해, inc() 함수가 호출될 때마다 전역 변수 count의 값이 1씩 증가합니다."
    },
    {
        "q": "[코드] 다음 Python '음수 슬라이싱' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [10, 20, 30, 40, 50]
            print(a[-3:-1])
        """),
        "answer": ["[30, 40]"],
        "explain": "음수 인덱스는 뒤에서부터 셉니다. (-1은 50, -2는 40, -3은 30). a[-3] (30)부터 a[-1] (50) *전*까지, 즉 [30, 40]이 출력됩니다."
    },
    # --- 심화 (Comprehension, Lambda, static, Pointer) (Set 8) ---
    {
        "q": "[코드] 다음 Python '람다(Lambda)'와 'filter' 함수 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3, 4, 5, 6]
            b = list(filter(lambda x: x % 2 == 0, a))
            print(b)
        """),
        "answer": ["[2, 4, 6]"],
        "explain": "filter 함수는 리스트 a의 요소 중 lambda 함수(x % 2 == 0, 즉 짝수)를 True로 만드는 값만 걸러냅니다."
    },
    {
        "q": "[코드] 다음 Python 'zip'과 '리스트 내포' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [1, 2, 3]
            b = ['A', 'B', 'C']
            c = [n * s for n, s in zip(a, b)]
            print(c)
        """),
        "answer": ["['A', 'BB', 'CCC']"],
        "explain": "zip(a, b)는 (1, 'A'), (2, 'B'), (3, 'C')를 짝지어줍니다. n * s는 문자열 반복을 의미합니다. (1*'A', 2*'B', 3*'C')"
    },
    {
        "q": "[코드] 다음 C언어 '포인터 연산' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[3] = {10, 20, 30};
                int *p = arr;
                printf("%d, ", *p++); // 후위
                printf("%d", *p);
                return 0;
            }
        """),
        "answer": ["10, 20", "10,20"],
        "explain": "*p++는 후위 연산입니다. *p (10)을 먼저 출력하고, 그 후에 포인터 p가 1 증가하여 arr[1] (20)을 가리킵니다."
    },
    {
        "q": "[코드] 다음 C언어 '포인터 연산' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            #include <stdio.h>
            int main() {
                int arr[3] = {10, 20, 30};
                int *p = arr;
                printf("%d, ", (*p)++); // 괄호
                printf("%d", arr[0]);
                return 0;
            }
        """),
        "answer": ["10, 11", "10,11"],
        "explain": "(*p)++는 p가 가리키는 *값*을 1 증가시킵니다. printf는 후위 연산이므로 현재 값 10을 먼저 출력하고, 그 후 arr[0]의 값이 11로 바뀝니다."
    },
    {
        "q": "[코드] 다음 C언어 '구조체 포인터' 함수 코드의 출력 결과는?\n\n" + textwrap.dedent("""
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
        "explain": "inc 함수에 p1의 주소(&p1)를 넘겼습니다. 포인터 p가 p1을 가리키므로, p->age는 p1.age를 의미합니다. (20 + 10 = 30)"
    },
    {
        "q": "[코드] 다음 Java 'static(정적) 변수/메소드' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
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
        "explain": "static 변수 a는 모든 객체가 공유합니다. static 메소드 add()가 호출되어 Main.a의 값이 10에서 20으로 변경되었습니다."
    },
    {
        "q": "[코드] 다음 Java '추상 클래스(abstract)' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            abstract class Animal {
                abstract void sound(); // 추상 메소드
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
        "explain": "추상 클래스 Animal을 상속받은 Dog 클래스가 추상 메소드 sound()를 'Bark'로 구현(오버라이딩)했습니다."
    },
    {
        "q": "[코드] 다음 Java 'super' 키워드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            class Parent {
                void sound() { System.out.println("Parent"); }
            }
            class Child extends Parent {
                @Override
                void sound() { 
                    super.sound(); // 1. 부모 sound() 호출
                    System.out.println("Child"); // 2. 자기 sound() 실행
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
        "explain": "자식(Child)의 sound()가 호출되었지만, 내부에서 super.sound()를 통해 부모(Parent)의 'Parent'가 먼저 출력되고, 그 다음 'Child'가 출력됩니다."
    },
    {
        "q": "[코드] 다음 Python 'global' 키워드 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            count = 0
            def inc():
                global count
                count += 1
            inc()
            inc()
            print(count)
        """),
        "answer": ["2"],
        "explain": "'global count' 키워드로 인해, inc() 함수가 호출될 때마다 전역 변수 count의 값이 1씩 증가합니다."
    },
    {
        "q": "[코드] 다음 Python '음수 슬라이싱' 코드의 출력 결과는?\n\n" + textwrap.dedent("""
            a = [10, 20, 30, 40, 50]
            print(a[-3:-1])
        """),
        "answer": ["[30, 40]"],
        "explain": "음수 인덱스는 뒤에서부터 셉니다. (-1은 50, -2는 40, -3은 30). a[-3] (30)부터 a[-1] (50) *전*까지, 즉 [30, 40]이 출력됩니다."
    },
    # --- AI 자동 생성 문제 ---
    {
        "q": '[문제 1] 다음 C 코드의 출력 결과는?\n\n#include <stdio.h>\n\nint main() {\n  int arr[5] = {10, 20, 30, 40, 50};\n  int *p = arr;\n  p++;\n  int result = *p + arr[2];\n  printf("%d", result);\n  return 0;\n}',
        "answer": ['50'],
        "explain": '포인터 p는 배열 arr의 시작 주소(arr[0])를 가리킵니다. `p++` 실행 후 p는 다음 요소인 arr[1]을 가리키게 됩니다. 따라서 역참조한 `*p`의 값은 20입니다. arr[2]의 값은 30이므로, 최종 결과는 `20 + 30 = 50` 입니다.'
    },
    {
        "q": '[문제 2] 다음 C 코드의 출력 결과는?\n\n#include <stdio.h>\n\nint main() {\n  int i, sum = 0;\n  for (i = 0; i < 3; i++) {\n    static int num = 10;\n    sum += num;\n    num++;\n  }\n  printf("%d", sum);\n  return 0;\n}',
        "answer": ['33'],
        "explain": 'static 지역 변수는 블록이 처음 실행될 때 한 번만 초기화되고, 이후에는 그 값이 유지됩니다. 따라서 num의 값은 10, 11, 12로 변하면서 sum에 누적됩니다. 최종 sum은 `10 + 11 + 12 = 33` 입니다.'
    },
    {
        "q": '[문제 3] 다음 C 코드의 출력 결과는?\n\n#include <stdio.h>\n\nint main() {\n  int a = 5, b = 3;\n  a = a ^ b;\n  b = a ^ b;\n  a = a ^ b;\n  printf("%d, %d", a, b);\n  return 0;\n}',
        "answer": ['3, 5'],
        "explain": '이 코드는 비트 XOR(^) 연산을 이용한 변수 값 교환(swap) 알고리즘입니다. 초기값 a=5, b=3이 세 번의 XOR 연산을 거치면서 서로 값이 바뀌게 됩니다. 따라서 최종적으로 a는 3, b는 5가 출력됩니다.'
    },
    {
        "q": '[문제 4] 다음 C 코드의 출력 결과는?\n\n#include <stdio.h>\n\nint main() {\n  int a = 5, b = 5;\n  int result = ++a + b--;\n  printf("%d, %d, %d", a, b, result);\n  return 0;\n}',
        "answer": ['6, 4, 11'],
        "explain": '`++a`는 전위 증가 연산자로, a의 값을 1 증가시킨 후(a=6) 연산에 사용합니다. `b--`는 후위 감소 연산자로, b의 현재 값(b=5)을 연산에 사용한 후 값을 1 감소시킵니다. 따라서 result는 `6 + 5 = 11`이 되며, 모든 연산이 끝난 후 a는 6, b는 4가 됩니다.'
    },
    {
        "q": '[문제 5] 다음 C 코드의 출력 결과는?\n\n#include <stdio.h>\n\nint main() {\n  int i = 0, sum = 0;\n  while (i < 5) {\n    sum += (i % 2 == 0) ? i : -i;\n    i++;\n  }\n  printf("%d", sum);\n  return 0;\n}',
        "answer": ['2'],
        "explain": 'while 루프는 i가 0부터 4까지 5번 반복됩니다. 삼항 연산자는 i가 짝수이면 i를, 홀수이면 -i를 sum에 더합니다. 따라서 sum의 계산 과정은 `0(i=0) + (-1)(i=1) + 2(i=2) + (-3)(i=3) + 4(i=4)`가 되어 최종 결과는 2입니다.'
    },
]