## ����

�A�����X�g�̐擪��\���ϐ�head���^�����܂��B���̘A�����X�g�ɃT�C�N�������݂��邩���ׂĂ��������B
�A�����X�g�̐擪����next�����ǂ��ĒT�����Ă������Ƃ��ɁA���łɌ��������Ƃ̂���m�[�h���ēx���������ꍇ�A�A�����X�g�ɃT�C�N�������݂���Ƃ����܂��B�T�C�N�������������ꍇtrue���A������Ȃ������ꍇfalse��Ԃ��Ă��������B

## �l��������

- ����l����A�����X�g��singly linked list�ł悳����
- Linked list
https://en.wikipedia.org/wiki/Linked_list
    - �A�����X�g�ɃT�C�N��������Ƃ������ƂƁACircular linked list�ł���Ƃ������Ƃ͕ʕ��݂���

- �T�C�N�������݂��Ȃ��ꍇ�Ƃ�
    - ���ׂĂ̘A�����X�g�̃m�[�h�𒲂ׂĂ��T�C�N���𔭌��ł��Ȃ������ꍇ�T�C�N�������݂��Ȃ������ƕ񍐂��Ă��悳�����B�T�C�N���𔭌������ꍇ������return�����肵�đ��݂��Ȃ��ꍇ�ƍ������Ȃ��悤�ɒ��ӂ���B

- ����m�[�h���ߋ������ς݂��ǂ������ׂ���@
    - ����܂ł̍�ƂŌ������m�[�h���������Ă����B�e��Ƃɂ����č���̍�ƂŌ������m�[�h����������Ă��邩���ׂ�B�ߋ��Ƀ�������Ă���΃T�C�N����񍐂��č�ƏI���B��������Ă��Ȃ���΃��������č�ƌp���B

- �^����ꂽ�A�����X�g�̐擪����m�[�h�����ɂ݂Ă����A�ߋ��ɔ����ς݂̃m�[�h���ēx�������ꍇ�͂����ŃT�C�N�������݂��Ă��邱�Ƃ�񍐂��č�ƏI���B�A�����X�g�̂��ׂẴm�[�h�𒲂ׂĂ��T�C�N����������Ȃ������ꍇ�A�T�C�N�����Ȃ��������Ƃ�񍐂��č�ƏI���B

- �v�Z��

    - �^����ꂽ�A�����X�g�̃m�[�h�̐���n�Ƃ���

    - ���Ԍv�Z�� 
        - O(n): �T�C�N����������ꍇ��������Ȃ��ꍇ���ׂẴm�[�h�𒲂ׂ邽�߁B

    - ��Ԍv�Z��
        - O(n): �T�C�N����������ꍇ���T�C�N����������Ȃ��ꍇ���ׂẴm�[�h�������ɕۑ�����邽�߁B

## Step1

```Python

class Solution:
    def hasCycle(self, head):
        detected_nodes = set()
        node = head
        while node:
            if node in detected_nodes:
                return True
            detected_nodes.add(node)
            node = node.next
        return False

```

- �ߋ����ׂ��m�[�h�̃����p��detected_nodes���悳�����Ǝv�������ǁA���̌��t���g���ƂȂ񂾂��傰���Ȃ��Ƃ�����ۂ�^���������ȂƎv�����B���ɗǂ����̂��Ȃ����T���B

    - https://dictionary.cambridge.org/dictionary/english/detect?q=detected
    > to notice something that is partly hidden or not clear, or to discover something, especially using a special method:

- �����܂�20�����炢�����������ȁB

## Step2

- ���̕��̃R�[�h�𒲂ׂ���R�����g�W���m�F����

- https://discord.com/channels/1084280443945353267/1195700948786491403/1195944696665604156
    - ���R�ȕ��@���ӎ����Ă���ƁA�t���C�h�̂������Ƃ��߂͎v�����Ȃ������B
- https://github.com/cheeseNA/leetcode/pull/6/files
    - set�̃n�b�V���֐����ǂ��Ȃ��Ă���̂��܂ŋ^��Ɏv��Ȃ������B�����������Ƃ��S�[���ɂ��Ȃ��悤���ӂ��悤�B
- https://github.com/momeemt/LeetCode/pull/1
    > ���Ԍv�Z�ʂ���A�����悻�̎��s���Ԃ𐄑���������͕�����܂��ł��傤���H
    - ���s���Ԃ܂ōl�����Ă��Ȃ������B
    - �ċA�̍l���͂Ȃ������B
- https://discord.com/channels/1084280443945353267/1183683738635346001/1204276545577943051
    > ���A�Ȃ�قǁA�v�Z�ʂƂ����T�O��m���Ă���Ȃ�΁A���Ƃ́A1���[�v�ŉ��N���b�N��(���b��)���l���āA��̓I�� n �ɂ�����b�����v�Z���邾���ł��B���N���b�N���ɂ��ẮA���Ȃ����̂ł����A������ւ�����Ă�����10�{���炢�̌덷�ōςނł��傤�B
    - ��Ōv�Z���Ă݂悤

- �t���C�h�̃A���S���Y���̐l�����ȁB

- https://github.com/TORUS0818/leetcode/blob/TORUS0818-patch-1/easy/141/answer.md
    - �������m�[�h����������f�[�^��found�Ƃ����Ă����B�V���v���B
- https://github.com/nittoco/leetcode/pull/12/files
    - visited_node�Ƃ����ϐ������������B�l�I�ɍD�݂�����nodes�̕����`�łȂ����R�͉����낤�B

```Python

class Solution:
    def hasCycle(self, head):
        visited_nodes = set()
        node = head
        while node:
            if node in visited_nodes:
                return True
            visited_nodes.add(node)
            node = node.next
        return False

```
- 2�����炢�ŉ��x�ł�������Ǝv���B

- �t���C�h�������Ă݂悤

## Step3

- �t���C�h��
    - ����͈���i�ރ|�C���^(slow)��2���i�ރ|�C���^(fast)��p�ӂ��āA��̃|�C���^���T�C�N���ɓ������ア����Ԃ���Ƃ������Ƃ������ɂ��Ă���悤�B
    - �T�C�N���̒��̕ӂ̐���M�Ƃ��āA�K���ȓ�̃m�[�h��slow��fast��u���Bslow����fast�܂Ŏ��v���ɂȂ����Ă���p�X�Ɋ܂܂��ӂ̐���k�Ƃ��āAslow����fast�܂Ŕ����v���ɂȂ����Ă���p�X�Ɋ܂܂��ӂ̐���M-k�Ƃ���B���[�v��i�ނ��Ƃɂ��A��҂̕ӂ̐���1�����Ă���BM-k�񃋁[�v���񂷂��Ƃ�slow��fast�̊Ԃ̕ӂ̐���0�ɂȂ�B���̂��Ƃ��烋�[�v���񂵂Ă����΂�����Ԃ��邱�Ƃ��ۏ؂���Ă���ƍl���Ă����̂��ȁB
- ���Ԍv�Z��: �T�C�N��������ꍇ�Aslow�|�C���^���T�C�N���ɓ����Ă���M-k�X�e�b�v�łԂ���Ǝv���̂ŁAO(n)
- ��Ԍv�Z��: �|�C���^����Ȃ̂�O(1)
```Python

class Solution:
    def hasCycle(self, head):
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

```
- �f���ɏ������炱���Ȃ����Bif���̈ʒu���C�ɂȂ�Bif���̈ʒu�����[�v���̐擪�Ɏ����Ă��邽�߂ɂ́Aslow��fast�̏����ʒu�����炳�Ȃ��Ƃ����Ȃ��B�ł����������fast�̏�������fast = head.next�Ƃ���O��head.next�����݂��邩�m�F���Ȃ��Ƃ����Ȃ��Ǝv���B

```Python

class Solution:
    def hasCycle(self, head):
        if head is None or head.next is None:
            return False
        slow = head
        fast = head.next
        while fast and fast.next:
            if slow == fast:
                return True
            slow = slow.next
            fast = fast.next.next
        return False

```
