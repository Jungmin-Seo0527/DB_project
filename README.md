# 플랫폼별 영화 정보 비교 웹 서비스

## 개요

네이버와 구글 플랫폼에서 실시간 인기 영화 리스트를 비교하고 영화에 대한 의견을 조회, 저장, 수정, 삭제 가능한 웹 어플리케이션

**디자인적 부분은 전혀 생각하지 않고 개발했음을 고려해주세요!!!!!**

## 사용 기술

* Flask
* selenium (crawling을 위한 라이브러리)
* SQLite
* HTML

## 데이터베이스 스키마

## 기능 설명

### 1. 메인 화면

![](https://i.ibb.co/CtrsmMS/image.jpg)

* 새로고침
    * 각각 구글과 네이버에서 구매 가능한 영화 정보를 새롭게 크롤링후 가공하에 데이터베이스에 저장
    * 언제든지 최신 목록을 랭킹순으로 조회 가능

* 플랫폼별 영화 리스트 조회
    * 각 플랫폼 별 랭킹순으로 정렬하여 화면에 보여줍니다.

* 제목으로 검색하기
    * 제목으로 검색하는 화면으로 이동

### 2. 영화 정보 자세히 보기

![](https://i.ibb.co/tcVtCcz/image.jpg)

* 가격정보, 장르, 평점(플랫폼 내에세의 평점), 바로가기 링크
* 내 리스트에 추가
    * 나의 평점, 의견을 남길 수 있습니다.

### 3. 나의 리스트 추가(의견 남기기)

![](https://i.ibb.co/Z1Zb6bJ/image.jpg)

* id
    * 기본키에 해당
* platform
    * 플랫폼을 구분짖는 키
    * 1: 구글, 2: 네이버
* id, platform, title 은 수정 불가능
* rate: 사용자가 남기는 평점
* commnet : 사용자가 남기는 의견
* Edit 버튼 클릭으로 저장

* 리스트 추가후의 영화 정보 조회 모습
  ![](https://i.ibb.co/fQMPK4R/image.jpg)

* Edit 로 수정 가능
* delete 로 삭제 가능

### 4. 제목으로 검색하기

![](https://i.ibb.co/LYNrF2g/image.jpg)

* 메인 화면에서 `제목으로 검색하기` 클릭
* 검색하고자 하는 영화 제목 작성후 `submit`버튼 클릭
* 검색 완료 화면
  ![](https://i.ibb.co/QfzGPtV/image.jpg)
    * 플랫폼별 랭킹, 별점, 가격 비교 가능
    * 원하는 플랫폼으로 바로가기 링크

## 아쉬운점







