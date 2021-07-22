/* eslint-disable @typescript-eslint/no-explicit-any */
import {HttpFunction} from '@google-cloud/functions-framework/build/src/functions';
import dotenv from 'dotenv';
import * as Storage from '@google-cloud/storage';
import {WebClient, LogLevel} from '@slack/web-api';

// GCP Storageの設定
/* cloud上にあるデータを取得している（過去のマッチの内容等）
   誰がマッチしたかを管理する方法を自分で考えて、どうやって保存していくかを決めて。
   どういう形式でファイルを残すのか考えて。（多分クラウドに上げた方がいい）
   json file がいいかな。
*/
const storage = new Storage.Storage({
  projectId: process.env.GOOGLE_CLOUD_PROJECT,
  keyFilename: process.env.GOOGLE_APPLICATION_CREDENTIALS,
});
const bucketName = 'shimokita-college-coffee-chat';

// 環境変数を読み込めるようにする
/* tokenを使って、特定の人しかいじれないようにする。環境変数はパソコンに残す。
　 （コードには書かないで、取得する）
　*/
dotenv.config();

// slack のクラスみたいの
const client = new WebClient(process.env.SLACK_BOT_TOKEN, {
  logLevel: LogLevel.DEBUG,
});

// list of removed users
const removedUsers = [
  // 第１回高校生ターム
  'U01T436SC68', // Rick Shinmi/リック
  'U01SZLWAFJM', // Ibuki Tadamasa
  'U01SM91A119', // Moe Shimizu
  'U01ST7LT6SG', // Luna Nakahara
  // 第2回高校生ターム
  'U01TUB6AG3X', // ideal(井上恵太)
  'U01UM7NJ52L', // Yuki Matsumoto
  'U01UA25NVG9', // Rina Mizushima
  'U01UA25PN3B', // 岩崎寿知(Junow Iwasaki)
  // インターン等でいない人
  'U01G1FRB62G', // Ayaka Ouchi (インターン)
  'U01MHE27AA0', // Dai Manabe
  'U01FS8CG05T', // Enya Toyama
  'U01FVH0JG1Z', // Eri Shimomukai
  'U01G9R2SN4E', // Nanami Furuya
  'U01FVAY1BR8', // Natsume Takahashi
  'U01GK6AE5PA', // Ryosuke Kobayashi
  'U01FU5836AF', // Ryoya Hattori
  'U01GK6A17HN', // Saya Takizawa
  'U01DAF9M97F', // SHINGO Umehara_梅原進吾
  'U01FQS0J6F7', // Aika Kotegawa
  'U01CYQX5EBH', // m.ueda
  'U01FD6TEYTH', // mew imashuku
  'U01FS8CEZ1T', // Sho Hayashi
  // Slack アプリケーション
  'U01FSD3EPDK', // Colla
  'U01JVMV6HK3', // 長期不在連絡
];

/**
 * これまでに作ってきたペアをすべて取り出して、配列の形にする関数
 *
 * @returns ペアの配列を返却
 */
const getHistoryData = async (): Promise<[string, string][]> => {
  const bucket = storage.bucket(bucketName);
  const [files] = await bucket.getFiles();
  const data: Array<[string, string]> = [];

  const getPairs = files.map(async file => {
    // ファイルをダウンロード
    const result = await file.download();
    // 元データBuffer => String => JSONにしてから、dataの中身のペアを一つずつ取り出す
    JSON.parse(result.toString()).data.map((pair: [string, string]) =>
      data.push(pair)
    );
  });
  await Promise.all(getPairs);

  return data;
};

/**
 * 新しく作った組み合わせが、今回作成しているペアの配列の中に重複していないかをチェックする関数
 *
 * @param 新しく作った組み合わせ
 * @param 今回作成した、ペアの配列
 * @returns もしひとつ以上入っていたら true | 入っていなければ false を返却
 */
const checkIsDuplicated = (
  newPair: [string, string],
  donePair: Array<[string, string]>
) => {
  let count = 0;
  donePair.map(pair => {
    const firstMember = newPair[0];
    const secondMember = newPair[1];
    if (pair.includes(firstMember) && pair.includes(secondMember)) {
      count += 1;
    }
  });

  return count >= 1;
};

/**
 * ペアを作成する関数
 * @param members
 * @returns 出来上がった、ペアの配列
 */
const createPairs = async (members: string[]) => {
  // 過去のペアリストを配列で取得
  const historyPair = await getHistoryData();
  // これから作るペアの配列の箱
  const pairlist: Array<[string, string]> = [];
  // pairlistがペアの配列になっているため、ペアを崩し、memberの名前の配列にする
  const doneUsers: Array<string> = [];
  // ランダム数字生成する関数
  const getNumber = () => Math.floor(Math.random() * members.length);

  const numberList = [...Array(members.length).keys()];
  // １から順番に回していく
  numberList.map(currentNumber => {
    // もし、今の番号が、pairlistの番号に含まれていたら、スキップ（その人はもうペア割り当て済み）
    if (doneUsers.includes(members[currentNumber])) return;
    let isLoop = true;
    // 人数の数の中からランダムな数字を生成し、添字として使う
    let pairNumber = getNumber();

    while (isLoop) {
      // もしpairに含まれていた場合、もしくは、添字が同じだった場合、再度ランダムな数字（添字）を生成する
      if (
        doneUsers.includes(members[pairNumber]) ||
        currentNumber === pairNumber
      ) {
        pairNumber = getNumber();
      } else {
        // 含まれていない、一緒でない場合
        const newPair: [string, string] = [
          members[currentNumber],
          members[pairNumber],
        ];
        // 過去のpairと照会して、重複チェック
        if (checkIsDuplicated(newPair, historyPair)) {
          // 存在した場合は再度ランダム数字生成（添字）
          pairNumber = getNumber();
        } else {
          isLoop = false;
          pairlist.push(newPair);
          doneUsers.push(members[currentNumber], members[pairNumber]);
        }
      }
    }
  });
  return pairlist;
};

/**
 * 今のmemberの数が偶数か奇数かを判定し、奇数ならば、一人を無作為に抽出して余った人を抜き出して2で割り切れる人数で返却する、偶数ならばそのまま返却する関数
 *
 * @param {プログラム実行時点のslackメンバー全員の名前を格納した配列}
 * @returns {removedUser?: 奇数だった場合に無作為に抽出したメンバー, newMembers: 奇数だった場合はremovedUserを抜き出して偶数にした配列、偶数だった場合はそのままmemberを返却}
 */
const checkIsDivaidable = (
  members: string[]
): {removedUser?: string; newMembers: string[]} => {
  if (members.length % 2 === 0) {
    const newMembers = members;
    return {newMembers};
  } else {
    const removedUser = members[Math.floor(Math.random() * members.length)];

    // TODO 将来的には、奇数の場合は３人グループを作るように修正する
    console.log(
      '================================================================'
    );
    console.log('removedUser', removedUser);
    console.log(
      '================================================================'
    );
    return {removedUser, newMembers: members.filter(m => m !== removedUser)};
  }
};

interface JsonDataInterface {
  executedDate: string;
  numberOfPair: number;
  removedUser: string;
  data: Array<[string, string]>;
  data2: Array<[string, string]>;
}

/**
 * 作成したペアの配列をjsonにして保存する関数
 * @param list 今回作成したペアの配列
 * @param removedUser メンバーの数が2で割り切れない数字だった場合の、無作為に抽出したメンバー
 */
const makeJson = (
  list: Array<[string, string]>,
  list2: Array<[string, string]>,
  removedUser = ''
) => {
  const d = new Date();
  const hour = d.getHours().toString().padStart(2, '0');
  const minutes = d.getMinutes().toString().padStart(2, '0');
  const formattedDate = `${d.getFullYear()}/${
    d.getMonth() + 1
  }/${d.getDate()} ${hour}:${minutes}`;
  const fileName = `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}.json`;

  const jsonData: JsonDataInterface = {
    executedDate: formattedDate,
    numberOfPair: list.length,
    removedUser: removedUser,
    data: list,
    data2: list2,
  };

  saveJson(jsonData, fileName);
};

const saveJson = async (jsonData: JsonDataInterface, fileName: string) => {
  const replacer = [
    'executedDate',
    'numberOfPair',
    'data',
    'data2',
    'removedUser',
  ]; // 改行を見やすくする（本当は配列をもう一つ改行を減らしたい）
  const strJson = JSON.stringify(jsonData, replacer, 2);
  const bucket = storage.bucket(bucketName);
  bucket.file(fileName).save(strJson, err => {
    if (!err) {
      console.log(`${fileName} is uploaded!`);
    }
  });
};

/**
 * DMを作成して組み合わせを伝える関数
 *
 * @param userId DMを投げるUserId
 */
const createDM = async (userId1: string, userId2: string) => {
  try {
    const openConversationPayload = {
      users: `${userId1},${userId2}`,
    };
    // DMのグループ作成
    const result1 = (await client.conversations.open(
      openConversationPayload
    )) as any;
    console.log('result of opening conversation', result1.ok);

    const postMessagePayload = {
      channel: result1.channel.id,
      text: `Hi! :wave: <@${userId1}> and <@${userId2}>\nコーヒーチャットの相手が決まったよ！\nコミュニケーションを取って、一週間以内に予定合わせて行ってきてね！ :coffee: :sandwich: :spaghetti: :cake: :rice_ball: :beer:`,
    };
    // 上記で作成したグループのIDに対してメッセージを投げる
    const result2 = await client.chat.postMessage(postMessagePayload);
    console.log('result of postMessage', result2.ok);
  } catch (err) {
    console.log('err', err);
  }
};

const createDMs = async (resultPairList: Array<[string, string]>) => {
  const postMessageFunc = resultPairList.map(
    async (pair: [string, string], index: number): Promise<void> => {
      const firstPerson = pair[0];
      const secondPerson = pair[1];
      // テスト用
      // if (firstPerson === 'U01SE27EDE2' || secondPerson === 'U01SE27EDE2') {
      //   // AkiとやっしーのID テスト用
      //   await createDM('U01KS3Z0WKV', 'U01SE27EDE2'); // テスト用
      // }

      // ローカルで開発するときはDM飛ばす関数を実行しないようにする
      const isProduction = process.env.MODE === 'production';
      console.log(
        `===================  ペアの組み合わせ  ${
          index + 1
        }  ================================`
      );
      console.log('firstPerson', firstPerson, 'secondPerson', secondPerson);
      if (isProduction) {
        await testFunc();
        await createDM(firstPerson, secondPerson);
      } else {
        await testFunc();
        console.log('ローカル開発環境');
      }
    }
  );

  await Promise.all(postMessageFunc);
};

// なぜかわからんが、gcp functionsにデプロイ時にcreateDMがコンパイルされない問題は、この関数を作って上記のisProfuctionのif文内で呼ばれるようにすると解決する
const testFunc = async () => {
  console.log(
    '================================================================'
  );
};

const main = async () => {
  const members: string[] = [];
  const result = (await client.users.list()).members as any;
  const idAndNames: {id: string; name: string}[] = [];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  result.map((r: any) => {
    const {id, is_bot, profile} = r;
    if (is_bot === true) return;

    idAndNames.push({
      id: id,
      name: profile.real_name,
    });
  });

  const getCollegeGeneralMembersPayload = {
    channel: 'C01DDPCC53M', // college_generalのチャンネル
    limit: 150,
  };

  const memberIDs = (
    await client.conversations.members(getCollegeGeneralMembersPayload)
  ).members as any;

  console.log('memberIDs', memberIDs.length);

  memberIDs.map((id: string) => {
    if (removedUsers.includes(id)) return;
    // const name = idAndNames.find(i => i.id === id)?.name as string;
    // if (name === undefined) {
    //   console.log('info', id);
    // }
    members.push(id);
  });

  console.log('members', members.length);
  const {removedUser, newMembers} = checkIsDivaidable(members);

  const resultPairList = await createPairs(newMembers);
  await createDMs(resultPairList);

  // IDのペアだとわかりにくいので、名前でのペアも作成してデータを残す
  const memberNameList: Array<[string, string]> = resultPairList.map(pair => {
    const name1 = idAndNames.find(i => i.id === pair[0])?.name as string;
    const name2 = idAndNames.find(i => i.id === pair[1])?.name as string;
    return [name1, name2];
  });

  if (removedUser) {
    makeJson(resultPairList, memberNameList, removedUser);
  } else {
    makeJson(resultPairList, memberNameList);
  }
};


// helloWorld が　APIとして実行される大本
export const helloWorld: HttpFunction = async (_req, _res) => {
  try {
    await main();
    _res.send({
      status: 'OK',
      content: '実行しました',
    });
  } catch (error) {
    console.error('error', error);
    _res.send({
      status: 'NG',
      content: 'エラーが発生しました',
    });
  }
};
