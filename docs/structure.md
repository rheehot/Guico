# Leaves

Guico 에는 크게 `4` 가지로 '잎' 을 분류합니다.

+ 형태
    + Colour <span style="color:#498DEB">#498DEB</span>
+ 이벤트
    + Colour <span style="color:#4CAF50">#4CAF50</span>
+ 소리
    + Colour <span style="color:#">#</span>
+ 일반
    + Colour <span style="color:#">#</span>

## 형태
시각적으로 변화를 만드는 잎들의 모음입니다.
예를 들어 _화면에 글쓰기_ 등이 있습니다.

## 이벤트
_프로그램이 시작되었을 때_ 등과 같이 특정한 상황을 가르키는 잎들의 모음입니다.
조건문과 같은 제어문에 종속되지 않습니다.

## 소리
_음악 재생하기_ 등의 잎이 이 분류에 속합니다.

## 일반
_변수_ 등과 같이 프로그래밍에서 공통으로 사용되는 요소들이 있습니다.

# interlanguage?
Guico 에서 만든 코드는 Python code 로 변환됩니다. 변환된 코드의 생김새는 다음과 같습니다:
```python
import Engine  # Guico 자체 엔진입니다.

def main():
    while Engine.loop:
        for event in Engine.pygame.event.get():
            Engine.Event(event)

        if Engine.is_key_pressed("k"):
            print("[k] KEY PRESSED")

        Engine.display.update()


if __name__ == "__main__":
    window = Engine.Window(size=(800, 600), title="Guico Window")
    main()


```